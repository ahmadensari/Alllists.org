"""Roles and capabilities (plan 11.2, appendix D). Roles are Django groups; subscriber is an entitlement, not a role."""

from django.contrib.auth.models import Group

ROLES = ["contributor", "surveyor", "surveyor_lead", "steward", "owner", "moderator", "finance", "admin"]
MFA_ROLES = {"moderator", "finance", "admin", "surveyor_lead"}

CAPS = {
    "add_entry": set(ROLES) | {"user"},
    "import_list": {"contributor", "steward", "moderator", "admin"},
    "verify": {"surveyor", "surveyor_lead", "moderator", "admin"},
    "edit_segment": {"steward", "moderator", "admin"},
    "claim_decide": {"moderator", "admin"},
    "company_content": {"owner", "moderator", "admin"},
    "moderate": {"moderator", "admin"},
    "takedown": {"moderator", "admin"},
    "edit_registries": {"admin"},
    "manage_users": {"admin"},
    "rate_phases": {"finance", "admin"},
    "create_payout": {"finance"},
    "approve_payout": {"finance"},
    "record_payment": {"finance", "admin"},
    "view_audit": {"moderator", "finance", "admin"},
    "run_extract": {"admin"},
    "staff_console": {"surveyor_lead", "moderator", "finance", "admin"},
}


def user_roles(user):
    if not getattr(user, "is_authenticated", False):
        return set()
    roles = set(user.groups.values_list("name", flat=True)) & set(ROLES)
    if user.is_superuser:
        roles.add("admin")
    return roles


def has_cap(user, cap):
    roles = user_roles(user)
    allowed = CAPS[cap]
    if "user" in allowed and getattr(user, "is_authenticated", False):
        return True
    return bool(roles & allowed)


def needs_mfa(user):
    return bool(user_roles(user) & MFA_ROLES) or user.is_staff


def grant_role(user, role):
    if role not in ROLES:
        raise ValueError(f"unknown role {role!r}")
    group, _ = Group.objects.get_or_create(name=role)
    user.groups.add(group)


def revoke_role(user, role):
    user.groups.remove(*Group.objects.filter(name=role))
