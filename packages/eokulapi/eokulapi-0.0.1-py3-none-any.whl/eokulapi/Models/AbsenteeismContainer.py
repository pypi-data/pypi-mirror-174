from dataclasses import dataclass
from typing import Optional

from eokulapi.Models import from_float, from_list, from_str, month_to_int
from eokulapi.Models.Absenteeism import Absenteeism


@dataclass
class AbsenteeismContainer:
    ozurlu: float
    ozursuz: float
    by_month: Optional[dict[int, float]]
    devamsizliklistesi: Optional[list[Absenteeism]]

    @staticmethod
    def from_dict(obj: dict) -> "AbsenteeismContainer":
        by_month: dict = {}
        ozurlu = from_float(float(from_str(obj.get("Ozurlu")).replace(",", ".")))
        ozursuz = from_float(float(from_str(obj.get("Ozursuz")).replace(",", ".")))

        for abs in obj.get("DevamsizlikGrafikler"):
            ay = from_str(abs.get("Ay"))
            gun = from_float(abs.get("GunSayisi"))
            ay_int = month_to_int(ay)
            by_month[ay_int] = gun

        liste = from_list(Absenteeism.from_dict, obj.get("DevamsizlikListesi"))
        return AbsenteeismContainer(ozurlu, ozursuz, by_month, liste)
