from typing import Any, Dict, Tuple, Iterable


def map_to_str(value: Any) -> str:
    return value if isinstance(value, str) else ""

def map_to_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}

def map_to_tuple_of_dicts(sequence: Iterable[Any]) -> Tuple[Dict[str, Any], ...]:
    if isinstance(sequence, tuple):
        return tuple(value for value in sequence if isinstance(value, dict))
    return ()

def normalize_str(value: str) -> str:
    return value.strip()
