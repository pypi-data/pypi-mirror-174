from dataclasses import dataclass
from typing import Optional

from eokulapi.Models import from_list
from eokulapi.Models.EndtermMark import EndtermMark


@dataclass
class EndtermMarkContainer:
    notlistesi: Optional[list[EndtermMark]]

    @staticmethod
    def from_dict(obj: dict) -> "EndtermMarkContainer":
        liste = from_list(EndtermMark.from_dict, obj.get("YilSonuNotListesi"))

        return EndtermMarkContainer(liste)
