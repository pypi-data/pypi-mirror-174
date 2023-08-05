from enum import Enum
from typing import Any, Callable, List, TypeVar

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def month_to_int(month: str) -> int:
    match month:
        case "OCAK" | "Ocak":
            return 1
        case "ŞUBAT" | "Şubat":
            return 2
        case "MART" | "Mart":
            return 3
        case "NİSAN" | "Nisan":
            return 4
        case "MAYIS" | "Mayıs":
            return 5
        case "HAZİRAN" | "Haziran":
            return 6
        case "TEMMUZ" | "Temmuz":
            return 7
        case "AĞUSTOS" | "Ağustos":
            return 8
        case "EYLÜL" | "Eylül":
            return 9
        case "EKİM" | "Ekim":
            return 10
        case "KASIM" | "Kasım":
            return 11
        case "ARALIK" | "Aralık":
            return 12
