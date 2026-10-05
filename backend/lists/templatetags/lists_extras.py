from django import template

register = template.Library()


@register.filter
def tr(strings, key):
    return strings.get(key, key)


@register.filter
def level_label(strings, level):
    return strings.get("level_" + (level or "none"), level)


@register.filter
def place_label(place, lang):
    return place.label(lang)


@register.simple_tag
def label(obj, lang):
    return obj.label(lang)
