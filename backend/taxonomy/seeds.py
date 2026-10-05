"""Seed list types, families and add-on templates from the decision log (section 8) and the component spec (section 6).
Safe to run twice. Individuals and children's services are created with their gates set, and the talent list is paused.
"""

from django.db import transaction

from .models import AddonField, AddonTemplate, Concept, ListTypeSettings
from .services import create_concept

F = AddonField.Type
# (key, type, validation, required_for_publish, show, filterable, row_descriptor)
FAMILIES = {
    "doctors": [
        ("specialty", F.TEXT, {"max_length": 120}, True, "P", True, True),
        ("qualifications", F.TEXT, {"max_length": 200}, False, "P", False, False),
        ("regulator_number", F.TEXT, {"max_length": 40}, False, "P", False, False),
        ("years_experience", F.NUMBER, {"min": 0, "max": 80}, False, "P", False, False),
        ("appointment_mode", F.ENUM, {"choices": ["walk_in", "appointment", "both"]}, False, "P", True, False),
        ("consultation_fee", F.MONEY, {}, False, "L", False, False),
        ("languages_spoken", F.CONCEPT_LIST, {}, False, "P", True, False),
        ("insurance_panels", F.CONCEPT_LIST, {}, False, "L", False, False),
    ],
    "hospitals": [
        (
            "facility_type",
            F.ENUM,
            {"choices": ["hospital", "clinic", "dispensary", "specialist_centre"]},
            True,
            "P",
            True,
            True,
        ),
        ("ownership", F.ENUM, {"choices": ["public", "private", "charity"]}, False, "P", True, False),
        ("licence_number", F.TEXT, {"max_length": 40}, False, "P", False, False),
        ("departments", F.CONCEPT_LIST, {}, False, "P", True, False),
        ("emergency_24x7", F.BOOL, {}, False, "P", True, False),
        ("accreditation", F.TEXT, {"max_length": 120}, False, "P", False, False),
        ("insurance_panels", F.CONCEPT_LIST, {}, False, "L", False, False),
    ],
    "labs_imaging": [
        ("centre_type", F.ENUM, {"choices": ["laboratory", "imaging", "both"]}, True, "P", True, True),
        ("modalities", F.CONCEPT_LIST, {}, False, "P", True, False),
        ("home_collection", F.BOOL, {}, False, "P", True, False),
        ("report_turnaround_hours", F.NUMBER, {"min": 0, "max": 720}, False, "P", False, False),
        ("accreditation", F.TEXT, {"max_length": 120}, False, "P", False, False),
        ("mri_field_strength_tesla", F.NUMBER, {"min": 0, "max": 12}, False, "P", False, False),
    ],
    "trades": [
        ("display_name", F.TEXT, {"max_length": 80}, False, "P", False, False),
        ("visit_charge", F.MONEY, {}, False, "L", False, False),
        ("emergency_service", F.BOOL, {}, False, "P", True, False),
        ("identity_verified", F.BOOL, {}, False, "P", True, False),
        ("years_in_trade", F.NUMBER, {"min": 0, "max": 80}, False, "P", False, False),
        ("warranty_days", F.NUMBER, {"min": 0, "max": 3650}, False, "P", False, False),
    ],
    "schools": [
        ("registration_body", F.TEXT, {"max_length": 80}, False, "P", False, False),
        ("grades", F.TEXT, {"max_length": 80}, True, "P", True, True),
        ("gender_mix", F.ENUM, {"choices": ["boys", "girls", "co_education"]}, False, "P", True, False),
        ("day_or_boarding", F.ENUM, {"choices": ["day", "boarding", "both"]}, False, "P", True, False),
        ("curriculum", F.TEXT, {"max_length": 80}, False, "P", True, False),
        ("monthly_fee", F.MONEY, {}, False, "L", False, False),
        ("fee_year", F.NUMBER, {"min": 1990, "max": 2100}, False, "L", False, False),
    ],
    "tutors": [
        ("subjects", F.CONCEPT_LIST, {}, True, "P", True, True),
        ("levels", F.CONCEPT_LIST, {}, False, "P", True, False),
        ("mode", F.ENUM, {"choices": ["home_visit", "online", "centre"]}, False, "P", True, False),
        ("hourly_rate", F.MONEY, {}, False, "L", False, False),
        ("trial_class", F.BOOL, {}, False, "P", False, False),
        ("qualification_checked", F.BOOL, {}, False, "P", True, False),
        ("background_check_date", F.DATE, {}, False, "P", False, False),
    ],
    "manufacturers": None,  # defined in services.seed_manufacturer_template
    "contractors": [
        ("registration_body", F.TEXT, {"max_length": 80}, False, "P", False, False),
        ("category", F.TEXT, {"max_length": 40}, False, "P", True, True),
        ("work_types", F.CONCEPT_LIST, {}, True, "P", True, False),
        ("project_size_band", F.ENUM, {"choices": ["small", "medium", "large"]}, False, "P", True, False),
        ("insurance_verified", F.BOOL, {}, False, "P", True, False),
        ("years_trading", F.NUMBER, {"min": 0, "max": 200}, False, "P", False, False),
    ],
    "real_estate": [
        ("agency_name", F.TEXT, {"max_length": 100}, False, "P", False, True),
        ("licence_number", F.TEXT, {"max_length": 40}, False, "P", False, False),
        ("areas_served", F.PLACE_LIST, {}, False, "P", True, False),
        ("listing_types", F.CONCEPT_LIST, {}, False, "P", True, False),
        ("years_experience", F.NUMBER, {"min": 0, "max": 80}, False, "P", False, False),
    ],
    "hotels": [
        ("property_type", F.ENUM, {"choices": ["hotel", "guest_house", "resort", "hostel"]}, True, "P", True, True),
        ("star_class", F.NUMBER, {"min": 0, "max": 7}, False, "P", True, False),
        ("rooms", F.NUMBER, {"min": 1, "max": 5000}, False, "P", False, False),
        ("check_in", F.TEXT, {"max_length": 10}, False, "P", False, False),
        ("check_out", F.TEXT, {"max_length": 10}, False, "P", False, False),
        ("amenities", F.CONCEPT_LIST, {}, False, "P", True, False),
        ("price_from", F.MONEY, {}, False, "L", False, False),
    ],
    "pharmacies_pumps": [
        ("brand", F.TEXT, {"max_length": 60}, False, "P", True, True),
        ("open_24x7", F.BOOL, {}, False, "P", True, False),
        ("delivery", F.BOOL, {}, False, "P", True, False),
        ("drug_licence", F.TEXT, {"max_length": 40}, False, "P", False, False),
        ("fuel_types", F.CONCEPT_LIST, {}, False, "P", True, False),
        ("ancillary_services", F.CONCEPT_LIST, {}, False, "P", False, False),
    ],
    "retail": [
        ("brands_carried", F.CONCEPT_LIST, {}, False, "P", True, True),
        ("delivery", F.BOOL, {}, False, "P", True, False),
        ("payment_methods", F.CONCEPT_LIST, {}, False, "P", False, False),
    ],
}

# family -> [(name, urdu, scale, template key, entity type, flags)]
HG, CT, NT, GL = "hyper_local", "city", "national", "global"
FAMILY_TREE = {
    "Health": [
        ("Doctors", "ڈاکٹر", HG, "doctors", "person", ("individual", "health"), ["physicians"]),
        ("Eye doctors", "آنکھوں کے ڈاکٹر", HG, "doctors", "person", ("individual", "health"), ["ophthalmologists"]),
        ("Nurses", "نرسیں", HG, "doctors", "person", ("individual", "health"), []),
        ("Hospitals", "ہسپتال", CT, "hospitals", "facility", ("health",), ["clinics"]),
        ("Eye hospitals", "آنکھوں کے ہسپتال", HG, "hospitals", "facility", ("health",), []),
        (
            "Medical stores and pharmacies",
            "میڈیکل سٹور اور فارمیسیاں",
            HG,
            "pharmacies_pumps",
            "business",
            ("health",),
            ["chemists", "drug stores"],
        ),
        (
            "MRI and imaging centres",
            "ایم آر آئی اور امیجنگ سینٹر",
            CT,
            "labs_imaging",
            "facility",
            ("health",),
            ["MRI machines", "radiology centres"],
        ),
        ("Laboratories", "لیبارٹریاں", CT, "labs_imaging", "facility", ("health",), ["diagnostic labs"]),
    ],
    "Education": [
        ("Schools", "سکول", CT, "schools", "institution", (), []),
        ("Quran tutors", "قرآن کے اساتذہ", HG, "tutors", "person", ("individual", "child"), ["Quran teachers"]),
        ("Tutors", "ٹیوٹر", HG, "tutors", "person", ("individual", "child"), ["private tutors"]),
        ("Bookshops", "کتابوں کی دکانیں", CT, "retail", "business", (), ["book stores"]),
    ],
    "Trades and services": [
        ("Plumbers", "پلمبر", HG, "trades", "person", ("individual",), ["pipe fitters"]),
        ("Electricians", "الیکٹریشن", HG, "trades", "person", ("individual",), []),
        ("Mobile phone repair", "موبائل فون کی مرمت", HG, "trades", "business", (), ["mobile repair services"]),
        ("Beauty parlours and salons", "بیوٹی پارلر اور سیلون", HG, "retail", "business", (), ["salons", "barbers"]),
        ("Contractors", "ٹھیکیدار", NT, "contractors", "business", (), ["builders"]),
        ("Real estate agents", "پراپرٹی ایجنٹ", CT, "real_estate", "business", (), ["property dealers"]),
        (
            "Data scientists",
            "ڈیٹا سائنس دان",
            GL,
            "doctors",
            "person",
            ("individual", "paused"),
            ["machine learning engineers"],
        ),
    ],
    "Manufacturing and trade": [
        ("Football makers", "فٹ بال بنانے والے", NT, "manufacturers", "business", (), ["soccer ball manufacturers"]),
        ("Fan makers", "پنکھے بنانے والے", NT, "manufacturers", "business", (), ["fan manufacturers"]),
        ("Sanitaryware makers", "سینیٹری ویئر بنانے والے", NT, "manufacturers", "business", (), []),
        ("Furniture makers", "فرنیچر بنانے والے", NT, "manufacturers", "business", (), ["furniture manufacturers"]),
        (
            "Factories and suppliers",
            "فیکٹریاں اور سپلائرز",
            NT,
            "manufacturers",
            "business",
            (),
            ["wholesale suppliers"],
        ),
    ],
    "Retail": [
        ("Bakeries", "بیکریاں", HG, "retail", "business", (), []),
        ("Mobile stores", "موبائل کی دکانیں", HG, "retail", "business", (), ["mobile phone shops"]),
        ("Spare parts shops", "اسپیئر پارٹس کی دکانیں", HG, "retail", "business", (), ["auto parts"]),
        ("Furniture stores", "فرنیچر کی دکانیں", CT, "retail", "business", (), []),
        ("Hardware shops", "ہارڈ ویئر کی دکانیں", HG, "retail", "business", (), []),
    ],
    "Hospitality and fuel": [
        ("Hotels", "ہوٹل", CT, "hotels", "business", (), ["guest houses"]),
        (
            "Petrol pumps",
            "پیٹرول پمپ",
            HG,
            "pharmacies_pumps",
            "business",
            (),
            ["gas station", "fuel station", "filling station"],
        ),
    ],
}
SURGICAL = (
    "Manufacturing and trade",
    (
        "Surgical instrument makers",
        "جراحی آلات بنانے والے",
        NT,
        "manufacturers",
        "business",
        (),
        ["surgical instruments manufacturers"],
    ),
)


@transaction.atomic
def seed_templates():
    from .services import seed_manufacturer_template

    seed_manufacturer_template()
    out = {}
    for key, spec in FAMILIES.items():
        tpl, _ = AddonTemplate.objects.get_or_create(
            key=key, defaults={"description": key.replace("_", " ").capitalize()}
        )
        out[key] = tpl
        for fkey, typ, validation, req, show, filt, row in spec or []:
            AddonField.objects.get_or_create(
                template=tpl,
                key=fkey,
                defaults=dict(
                    label_key=f"addon.{key}.{fkey}",
                    type=typ,
                    validation=validation,
                    required_for_publish=req,
                    show=show,
                    filterable=filt,
                    row_descriptor=row,
                ),
            )
    return out


@transaction.atomic
def seed_list_types():
    templates = seed_templates()
    tree = {k: list(v) for k, v in FAMILY_TREE.items()}
    tree[SURGICAL[0]].insert(0, SURGICAL[1])
    made = 0
    for family_name, items in tree.items():
        fam = Concept.objects.filter(
            kind="family", slug=family_name.lower().replace(" ", "-")
        ).first() or create_concept(kind=Concept.Kind.FAMILY, name=family_name)
        for name, ur, scale, tpl_key, entity, flags, synonyms in items:
            existing = Concept.objects.filter(kind="list_type", labels__text=name).first()
            if existing:
                continue
            c = create_concept(
                kind=Concept.Kind.LIST_TYPE,
                name=name,
                parent=fam,
                natural_scale=scale,
                template=templates.get(tpl_key),
                entity_type_default=entity,
                synonyms=list(synonyms) + [(ur, "ur")],
                status="paused" if "paused" in flags else "active",
            )
            from .models import ConceptLabel
            from core.textfold import fold

            ConceptLabel.objects.create(concept=c, language="ur", kind="preferred", text=ur, text_fold=fold(ur))
            ListTypeSettings.objects.filter(concept=c).update(
                is_individual="individual" in flags,
                is_child_facing="child" in flags,
                is_health="health" in flags,
                share_hidden="individual" in flags or "child" in flags,
            )
            made += 1
    return made
