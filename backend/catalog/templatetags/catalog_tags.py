from django import template
from django.utils import timezone

from catalog import format as fmt
from catalog import strings

register = template.Library()


@register.simple_tag(takes_context=True)
def tr(context, key, **kw):
    return strings.t(context["lang"], key, **kw)


@register.simple_tag(takes_context=True)
def u(context, path):
    """Prefix an internal address with the language prefix."""
    return context.get("prefix", "") + path


@register.simple_tag(takes_context=True)
def date(context, value):
    return fmt.fmt_date(context["lang"], value)


@register.simple_tag(takes_context=True)
def age(context, value):
    return fmt.age_text(context["lang"], value, timezone.now().date())


@register.simple_tag(takes_context=True)
def pname(context, place):
    return place.name_for(context["lang"])


@register.simple_tag(takes_context=True)
def clabel(context, concept):
    return concept.label(context["lang"])


@register.filter
def get(d, key):
    return d.get(key, "") if hasattr(d, "get") else ""


@register.filter
def humanize(key):
    return str(key).replace("_", " ").capitalize()


@register.simple_tag(takes_context=True)
def addon_label(context, key):
    k = f"addon_{key}"
    return strings.t(context["lang"], k) if k in strings.EN else str(key).replace("_", " ").capitalize()


@register.simple_tag(takes_context=True)
def enum_label(context, value):
    k = f"enum_{value}"
    return strings.t(context["lang"], k) if isinstance(value, str) and k in strings.EN else value
