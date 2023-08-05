from dataclasses import dataclass

from eokulapi.Models import from_int, from_str
from eokulapi.Models.AvgMark import AvgMark


@dataclass
class AvgMarkLesson:
    ders: str
    donem: int
    marks: dict[int, AvgMark]

    @staticmethod
    def from_dict(obj: dict) -> "AvgMarkLesson":
        ders = from_str(obj.get("DERS"))
        donem = from_int(int(from_str(obj.get("DONEM"))))
        marks = {}
        for i in range(1, 7):
            if obj.get(f"Y{i}SUBEORT") == "":
                avg = None
            else:
                avg = float(obj.get(f"Y{i}SUBEORT").replace(",", "."))
            mark = AvgMark.from_dict(
                {
                    "value": obj.get(f"Y{i}"),
                    "description": obj.get(f"Y{i}ACIKLAMA"),
                    "description_value": obj.get(f"Y{i}ACIKLAMADEGER"),
                    "avg_mark": avg,
                }
            )
            marks[i] = mark
            return AvgMarkLesson(ders, donem, marks)
