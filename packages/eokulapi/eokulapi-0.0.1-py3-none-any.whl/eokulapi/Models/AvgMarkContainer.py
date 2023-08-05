from dataclasses import dataclass

from eokulapi.Models import from_list
from eokulapi.Models.AvgMarkLesson import AvgMarkLesson


@dataclass
class AvgMarkContainer:
    liste: list[AvgMarkLesson]

    @staticmethod
    def from_dict(obj: dict) -> "AvgMarkContainer":
        liste = from_list(AvgMarkLesson.from_dict, obj.get("YaziliOrtalamaListesi"))

        return AvgMarkContainer(liste)
