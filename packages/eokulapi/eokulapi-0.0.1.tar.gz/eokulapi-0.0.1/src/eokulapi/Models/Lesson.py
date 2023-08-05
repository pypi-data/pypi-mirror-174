from dataclasses import dataclass
from datetime import datetime

from eokulapi.Models import from_int, from_none, from_str, from_union


@dataclass
class Lesson:
    start: datetime.time
    end: datetime.time
    name: str
    nth: int
    teacher: str | None

    @staticmethod
    def from_dict(obj: dict) -> "Lesson":
        start = from_str(obj.get("Baslangic_Saati"))
        end = from_str(obj.get("Bitis_Saati"))
        name = from_str(obj.get("Ders"))
        nth = from_int(obj.get("KacinciDers"))
        teacher = from_union([from_str, from_none], obj.get("Ogretmen"))
        if isinstance(teacher, str) and teacher[0] == " ":
            teacher = teacher[1:]
        return Lesson(start, end, name, nth, teacher)
