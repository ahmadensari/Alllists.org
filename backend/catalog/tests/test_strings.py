from catalog import strings
from catalog.strings.en import EN
from catalog.strings.ur import UR


def test_placeholders_match_between_languages():
    assert strings.placeholder_mismatches() == []


def test_no_stray_urdu_keys():
    assert set(UR) <= set(EN)


def test_plural_selection_and_fallback():
    assert strings.t("en", "n_entries", n=1) == "1 entry" and strings.t("en", "n_entries", n=3) == "3 entries"
    assert strings.t("ur", "n_entries", n=1) == "1 اندراج"
    assert strings.t("ur", "addon_tax_ids") == strings.t(
        "en", "addon_tax_ids"
    )  # untranslated key falls back to English


def test_titles_follow_the_specified_pattern():
    assert (
        strings.t("en", "title_entry", name="Acme", list_type="Surgical", place="Sialkot")
        == "Acme – Surgical in Sialkot – AllLists"
    )
    assert strings.t("en", "title_list", list_type="Surgical", place="Sialkot") == "Surgical in Sialkot – AllLists"


def test_all_labels_are_whole_sentences_with_named_placeholders():
    for key, value in EN.items():
        texts = value.values() if isinstance(value, dict) else [value]
        for text in texts:
            assert "{}" not in text and "%s" not in text, key


def test_the_four_check_labels_only():
    labels = {k: EN[k] for k in EN if k.startswith("level_") and not k.endswith("_help")}
    assert labels == {
        "level_surveyor": "Surveyor-verified",
        "level_owner": "Owner-verified",
        "level_ai": "AI-checked",
        "level_none": "Not verified yet",
    }
    assert "Verified" not in {EN["level_ai"], EN["level_none"]}
