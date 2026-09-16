import re


DATASET_VERSION = "2026-09-15"
DATASET_SOURCE = "NH Switch Guide / GBATemp community serial data"


# Values are the first six digits after the three-letter serial family.
# Example:
# XAW10065000000 -> family XAW, value 100650
#
# unpatched_max is exclusive for our classification:
# value < unpatched_max = UNPATCHED
# unpatched_max <= value < patched_min = POSSIBLY PATCHED
# value >= patched_min = PATCHED
SERIAL_RANGES = {
    "XAW1": {
        "unpatched_max": 100650,
        "patched_min": 101200,
        "unpatched_display": "XAW10065000000",
        "patched_display": "XAW10120000000",
    },
    "XAW4": {
        "unpatched_max": 400110,
        "patched_min": 400125,
        "unpatched_display": "XAW40011000000",
        "patched_display": "XAW40012500000",
    },
    "XAW7": {
        "unpatched_max": 700175,
        "patched_min": 700300,
        "unpatched_display": "XAW70017500000",
        "patched_display": "XAW70030000000",
    },
    "XAJ1": {
        "unpatched_max": 100200,
        "patched_min": 100300,
        "unpatched_display": "XAJ10020000000",
        "patched_display": "XAJ10030000000",
    },
    "XAJ4": {
        "unpatched_max": 400440,
        "patched_min": 400830,
        "unpatched_display": "XAJ40044000000",
        "patched_display": "XAJ40083000000",
    },
    "XAJ7": {
        "unpatched_max": 700400,
        "patched_min": 700500,
        "unpatched_display": "XAJ70040000000",
        "patched_display": "XAJ70050000000",
    },
}


POTENTIALLY_PATCHED_PREFIXES = {
    "XAW9",
    "XAJ9",
    "XAK1",
    "XAK4",
    "XAK7",
    "XAK9",
}


def normalize_serial(serial):
    """Normalize a Nintendo Switch serial entered by the user."""
    if not serial:
        return ""

    return re.sub(r"[^A-Z0-9]", "", serial.upper())


def check_serial(serial):
    normalized = normalize_serial(serial)

    result = {
        "serial": normalized,
        "status": "UNKNOWN",
        "prefix": None,
        "message": "",
        "range_info": None,
        "dataset_version": DATASET_VERSION,
        "dataset_source": DATASET_SOURCE,
    }

    if len(normalized) < 9:
        result["message"] = "Enter a complete Nintendo Switch serial number."
        return result

    family = normalized[:3]

    if family not in ("XAW", "XAJ", "XAK"):
        result["prefix"] = normalized[:4]
        result["message"] = (
            "This serial is not present in the supported fusee-gelee "
            "serial database and should not be considered vulnerable."
        )
        return result

    digits = normalized[3:]

    if not digits.isdigit() or len(digits) < 6:
        result["message"] = "The serial number format is invalid."
        return result

    # NH Switch Guide uses the first six digits after XAW/XAJ/XAK.
    serial_value = int(digits[:6])
    prefix = family + digits[0]

    result["prefix"] = prefix

    if prefix in SERIAL_RANGES:
        ranges = SERIAL_RANGES[prefix]

        result["range_info"] = {
            "unpatched_max": ranges["unpatched_display"],
            "patched_min": ranges["patched_display"],
        }

        if serial_value < ranges["unpatched_max"]:
            result["status"] = "UNPATCHED"
            result["message"] = (
                "This serial falls inside the known unpatched range. "
                "The console should be vulnerable to fusee-gelee via RCM."
            )

        elif serial_value >= ranges["patched_min"]:
            result["status"] = "PATCHED"
            result["message"] = (
                "This serial falls inside the known patched range. "
                "The console is not vulnerable to fusee-gelee via RCM."
            )

        else:
            result["status"] = "POSSIBLY PATCHED"
            result["message"] = (
                "This serial falls inside the transition range. "
                "The serial number alone cannot determine whether this "
                "console is patched."
            )

        return result

    if prefix in POTENTIALLY_PATCHED_PREFIXES:
        result["status"] = "POSSIBLY PATCHED"
        result["message"] = (
            "This serial prefix is listed as potentially patched. "
            "The serial number alone cannot confirm exploitability."
        )
        return result

    result["status"] = "PATCHED"
    result["message"] = (
        "This serial is not in a known vulnerable range. "
        "It should not be considered vulnerable to fusee-gelee."
    )

    return result