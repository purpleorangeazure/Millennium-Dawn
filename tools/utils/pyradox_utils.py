

def normalize_type(value: object) -> list[str]:
    """Treat HOI4 type values as a list of string tokens."""
    normalized = normalize_node(value)
    if normalized is None:
        return []
    if isinstance(normalized, str):
        return [normalized]
    if isinstance(normalized, (list, tuple, set)):
        return [str(item) for item in normalized]
    return [str(normalized)]


def dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    """Deduplicate a sequence while preserving first-seen order."""
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def as_mapping(value: object) -> dict[str, object]:
    """Normalize and validate a value as a string-keyed mapping."""
    normalized = normalize_node(value)
    if isinstance(normalized, dict):
        return {str(key): inner for key, inner in normalized.items()}
    raise TypeError(f"Expected mapping but got {type(value)!r}")


def token_list(value: object) -> list[str]:
    """Flatten nested scalar/list/dict values into a token list of strings."""
    normalized = normalize_node(value)
    if normalized is None:
        return []
    if isinstance(normalized, str):
        return [normalized]
    if isinstance(normalized, (int, float, bool)):
        return [str(normalized)]
    if isinstance(normalized, list):
        tokens: list[str] = []
        for item in normalized:
            tokens.extend(token_list(item))
        return tokens
    if isinstance(normalized, dict):
        tokens = []
        for item in normalized.values():
            tokens.extend(token_list(item))
        return tokens
    return [str(normalized)]


def as_trait_list(value: object) -> list[dict[str, object]]:
    """Normalize trait payloads to a list of trait dictionaries."""
    normalized = normalize_node(value)
    if normalized is None:
        return []
    if isinstance(normalized, dict):
        return [cast(dict[str, object], normalized)]
    if isinstance(normalized, list):
        traits: list[dict[str, object]] = []
        for item in normalized:
            if isinstance(item, dict):
                traits.append(cast(dict[str, object], item))
        return traits
    return []


def stats_value(value: object) -> object:
    """Coerce common script scalar forms into Python bool/int/float values."""
    normalized = normalize_node(value)
    if isinstance(normalized, str):
        lowered = normalized.strip().lower()
        if lowered in {"yes", "true", "on"}:
            return True
        if lowered in {"no", "false", "off"}:
            return False
        try:
            if "." in lowered:
                return float(lowered)
            return int(lowered)
        except ValueError:
            return normalized
    return normalized


__all__ = [
    "as_mapping",
    "as_trait_list",
    "dedupe_preserve_order",
    "normalize_bool",
    "normalize_node",
    "normalize_scalar",
    "normalize_type",
    "parse_file",
    "stats_value",
    "token_list",
]
