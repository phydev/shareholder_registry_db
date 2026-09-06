import logging
import re

logger = logging.getLogger(__name__)


def parse_address(address: str) -> tuple[dict, bool]:
    parsed_address = {"postal_code": None, "location": None}
    needs_review = False

    address = address.strip().strip("\"'")
    if not address:
        return parsed_address, needs_review

    all_codes = re.findall(r"\d+", address)
    if all_codes:
        parsed_address["postal_code"] = all_codes[0]
        if len(set(all_codes)) > 1:
            needs_review = True

    text_only = re.sub(r"\d+", " ", address)

    text_only = re.sub(r"\s+,\s*", ", ", text_only)

    words = text_only.split()
    seen = set()
    unique_words = []

    for word in words:
        word_clean = word.upper().strip(" ,")
        if not word_clean:
            continue

        if word_clean not in seen:
            seen.add(word_clean)
            unique_words.append(word)
        else:
            needs_review = True

    if unique_words:
        location = " ".join(unique_words).strip()
        location = re.sub(r"\s+,\s*", ", ", location)
        parsed_address["location"] = location
    else:
        parsed_address["location"] = None

    return parsed_address, needs_review
