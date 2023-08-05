from dataclasses import dataclass
from typing import Optional

from eokulapi.Models import from_list
from eokulapi.Models.MarkLesson import MarkLesson


@dataclass
class MarkContainer:
    notlistesi: Optional[list[MarkLesson]]

    @staticmethod
    def from_dict(obj: dict) -> "MarkContainer":
        liste = from_list(MarkLesson.from_dict, obj.get("notListesi"))
        return MarkContainer(liste)
