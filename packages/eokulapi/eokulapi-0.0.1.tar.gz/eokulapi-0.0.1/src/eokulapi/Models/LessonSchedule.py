from dataclasses import dataclass
from typing import Optional

from eokulapi.Models import from_list
from eokulapi.Models.Day import Day


@dataclass
class LessonSchedule:
    liste: Optional[list[Day]]

    @staticmethod
    def from_dict(obj: dict) -> "LessonSchedule":
        liste = from_list(Day.from_dict, obj.get("DersProgramiListesi"))
        return LessonSchedule(liste)
