from typing import Any, Dict, Tuple, Iterable

def map_to_str(_value: Any) -> str:
    return _value if isinstance(_value, str) else ""

def map_to_dict(_value: Any) -> Dict[str, Any]:
    return _value if isinstance(_value, dict) else {}

def map_to_tuple_of_dicts(_sequence: Iterable[Any]) -> Tuple[Dict[str, Any], ...]:
    if isinstance(_sequence, tuple):
        return tuple(_sequence_value for _sequence_value in _sequence if isinstance(_sequence_value, dict))
    return ()

def normalize_str_case_sensitive(_value: str) -> str:
    return map_to_str(_value).strip()

def normalize_str_case_insensitive(_value: str) -> str:
    return normalize_str_case_sensitive(_value).lower()
