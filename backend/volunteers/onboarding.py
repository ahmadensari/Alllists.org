"""Contributor onboarding (plan P2.21): the rules in five questions. Passing records the date and unlocks surveyor tasks."""

from django.db import transaction

from core import clock
from core.models import audit

from .services import ensure_profile

PASS_MARK = 4  # of 5

# (key, {lang: question}, [(answer key, {lang: text})], right answer key)
QUESTIONS = [
    (
        "contacts",
        {
            "en": "A buyer asks you for a shop's phone number from the platform. What do you do?",
            "ur": "ایک خریدار پلیٹ فارم سے کسی دکان کا فون نمبر مانگتا ہے۔ آپ کیا کریں گے؟",
        },
        [
            ("a", {"en": "Send it, the buyer is paying", "ur": "بھیج دوں، خریدار ادائیگی کر رہا ہے"}),
            ("b", {"en": "Never share it; point to the message button", "ur": "کبھی نہیں؛ پیغام کا بٹن بتا دوں"}),
        ],
        "b",
    ),
    (
        "rights",
        {
            "en": "You want to upload a list you bought from a data seller. Is that allowed?",
            "ur": "آپ ڈیٹا بیچنے والے سے خریدی ہوئی فہرست اپ لوڈ کرنا چاہتے ہیں۔ کیا یہ جائز ہے؟",
        },
        [
            ("a", {"en": "Only if I have the right to share it", "ur": "صرف اگر مجھے اسے شیئر کرنے کا حق ہو"}),
            ("b", {"en": "Yes, once I own the file", "ur": "ہاں، فائل میری ہو تو"}),
        ],
        "a",
    ),
    (
        "independence",
        {
            "en": "Can you verify an entry that you added yourself?",
            "ur": "کیا آپ اپنی شامل کی ہوئی اندراج کی خود تصدیق کر سکتے ہیں؟",
        },
        [
            ("a", {"en": "Yes, I know it best", "ur": "ہاں، میں اسے سب سے بہتر جانتا ہوں"}),
            ("b", {"en": "No, someone else must check it", "ur": "نہیں، کسی اور کو جانچنا ہوگا"}),
        ],
        "b",
    ),
    (
        "evidence",
        {
            "en": "You called a shop and nobody answered. What do you record?",
            "ur": "آپ نے دکان کو فون کیا اور کسی نے جواب نہ دیا۔ آپ کیا لکھیں گے؟",
        },
        [
            ("a", {"en": "Unreachable, with the time and number tried", "ur": "رابطہ نہیں ہوا، وقت اور نمبر کے ساتھ"}),
            ("b", {"en": "Confirmed, it is probably fine", "ur": "تصدیق ہو گئی، غالباً ٹھیک ہے"}),
        ],
        "a",
    ),
    (
        "people",
        {
            "en": "A tutor gives you her home address for the list. What goes on the public page?",
            "ur": "ایک ٹیوٹر آپ کو گھر کا پتہ دیتی ہے۔ عوامی صفحے پر کیا آئے گا؟",
        },
        [
            ("a", {"en": "The area only, never the home address", "ur": "صرف علاقہ، گھر کا پتہ کبھی نہیں"}),
            ("b", {"en": "The full address, it helps buyers", "ur": "پورا پتہ، اس سے خریداروں کو مدد ملتی ہے"}),
        ],
        "a",
    ),
]


def questions(lang="en"):
    return [
        {"key": k, "text": q.get(lang, q["en"]), "answers": [(a, t.get(lang, t["en"])) for a, t in answers]}
        for k, q, answers, _ in QUESTIONS
    ]


def score(answers):
    return sum(1 for k, _, _, right in QUESTIONS if answers.get(k) == right)


@transaction.atomic
def submit(user, answers, *, declared_rights):
    """Record the rights declaration and the quiz. Returns (score, passed). A person may retry any time."""
    prof = ensure_profile(user)
    s = score(answers)
    prof.quiz_score = s
    if declared_rights and prof.declared_rights_at is None:
        prof.declared_rights_at = clock.now()
    passed = bool(declared_rights) and s >= PASS_MARK
    if passed and prof.onboarded_at is None:
        prof.onboarded_at = clock.now()
        audit("contributor.onboarded", actor=user, object_type="user", object_uid=str(user.pk), payload={"score": s})
    prof.save()
    return s, passed


def is_onboarded(user):
    return ensure_profile(user).onboarded_at is not None
