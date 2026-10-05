"""Dates, ages and numbers for pages. Western digits in every language (decision); Urdu gets Urdu month names."""

import datetime

from . import strings

MONTHS = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "ur": ["جنوری", "فروری", "مارچ", "اپریل", "مئی", "جون", "جولائی", "اگست", "ستمبر", "اکتوبر", "نومبر", "دسمبر"],
}


def fmt_date(lang, value):
    if value is None:
        return ""
    if isinstance(value, datetime.datetime):
        value = value.date()
    return f"{value.day} {MONTHS[lang][value.month - 1]} {value.year}"


def age_text(lang, value, today):
    if value is None:
        return ""
    if isinstance(value, datetime.datetime):
        value = value.date()
    days = (today - value).days
    if days <= 0:
        return strings.t(lang, "age_today")
    if days < 14:
        return strings.t(lang, "age_days", n=days)
    if days < 60:
        return strings.t(lang, "age_weeks", n=days // 7)
    if days < 730:
        return strings.t(lang, "age_months", n=days // 30)
    return strings.t(lang, "age_years", n=days // 365)
