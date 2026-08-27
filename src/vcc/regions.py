from __future__ import annotations


REGION_GROUPS = {
    "USA": {
        "AR", "BR", "CA", "CL", "CO", "MX", "PE", "US",
    },
    "EUR": {
        "AT", "BE", "BG", "CH", "CY", "CZ", "DE", "DK", "EE",
        "ES", "FI", "FR", "GB", "GR", "HR", "HU", "IE", "IL",
        "IT", "LT", "LU", "LV", "MT", "NL", "NO", "PL", "PT",
        "RO", "RU", "SE", "SI", "SK", "ZA",
    },
    "ASIA": {"CN", "HK", "KR", "SG", "TW"},
    "JPN": {"JP"},
    "AUS": {"AU", "NZ"},
}


def base_title_id(title_id: str) -> str:
    """Return the base-family ID used by updates and DLC."""

    normalized = str(title_id).strip().upper()
    if len(normalized) != 16:
        return normalized
    return normalized[:13] + "000"


def classify_region(source_region=None, countries=None) -> str:
    """Convert TitleDB country codes to a compact display region."""

    primary = str(source_region or "").strip().upper()
    for label, codes in REGION_GROUPS.items():
        if primary in codes or primary == label:
            return label

    labels = {
        label
        for country in (countries or [])
        for label, codes in REGION_GROUPS.items()
        if str(country).strip().upper() in codes
    }

    if len(labels) == 1:
        return labels.pop()
    if len(labels) > 1:
        return "MULTI"
    return "UNKNOWN"
