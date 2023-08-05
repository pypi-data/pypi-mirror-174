from dataclasses import dataclass

from eokulapi.Models import from_list, from_str
from eokulapi.Models.Lesson import Lesson


@dataclass
class Day:
    day: int
    LessonList: list[Lesson]

    @staticmethod
    def from_dict(obj: dict) -> "Day":
        liste = from_list(Lesson.from_dict, obj.get("DersProgramiItemList"))
        match from_str(obj.get("Gun")):
            case "Pazartesi":
                day = 0
            case "Salı":
                day = 1
            case "Çarşamba":
                day = 2
            case "Perşembe":
                day = 3
            case "Cuma":
                day = 4
            case "Cumartesi":
                day = 5
            case "Pazar":
                day = 6
        return Day(day, liste)
