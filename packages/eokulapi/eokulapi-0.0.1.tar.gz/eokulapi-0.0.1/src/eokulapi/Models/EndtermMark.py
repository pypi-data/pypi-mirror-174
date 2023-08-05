from dataclasses import dataclass

from eokulapi.Models import from_float, from_str


@dataclass
class EndtermMark:
    ogretimyili: str
    sinif: str
    yilsonunotu: float

    @staticmethod
    def from_dict(obj: dict) -> "EndtermMark":
        yil = from_str(obj.get("OGRETIMYILI"))
        sinif = from_str(obj.get("SINIF"))
        yilsonunot = from_float(float(from_str(obj.get("YILSONUNOTU")).replace(",", ".")))
        return EndtermMark(yil, sinif, yilsonunot)
