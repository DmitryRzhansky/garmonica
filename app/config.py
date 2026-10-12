import os


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-nova-clinic")
    JSON_AS_ASCII = False
    # Staging gate: HTML pages are not served until the password is entered.
    SITE_PASSWORD_PROTECT = _env_flag("SITE_PASSWORD_PROTECT", True)
    SITE_ACCESS_PASSWORD = os.environ.get("SITE_ACCESS_PASSWORD", "nova-clinic-test")
