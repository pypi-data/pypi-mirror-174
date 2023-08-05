from dataclasses import dataclass
from typing import Any

from eokulapi.Models import from_float, from_int, from_str


@dataclass
class MarkLesson:
    ders: str
    derskodu: str
    derssaati: int
    donem: int
    muaf: bool
    ODV: Any
    TPU: Any
    puan: float
    sozlu: dict[int, float]
    yazili: dict[int, float]

    @staticmethod
    def from_dict(obj: dict) -> "MarkLesson":
        ders = from_str(obj.get("Ders"))
        ders_kodu = from_str(obj.get("DersKodu"))
        ders_saati = from_int(int(from_str(obj.get("DersSaati"))))
        donem = from_int(int(from_str(obj.get("Donem"))))
        muaf = False if from_str(obj.get("Muaf")) == "-" else True
        odv = obj.get("ODV")
        tpu = obj.get("TPU")
        puan = from_float(float(from_str(obj.get("PUANI")).replace(",", ".")))

        sozlu: dict[int, float] = {}
        yazili: dict[int, float] = {}

        for i in range(1, 7):
            dat = from_str(obj.get(f"SZL{i}"))
            if dat:
                sozlu[i] = float(dat.replace(",", "."))
        for i in range(1, 7):
            dat = from_str(obj.get(f"Y{i}"))
            if dat:
                yazili[i] = float(dat.replace(",", "."))

        return MarkLesson(ders, ders_kodu, ders_saati, donem, muaf, odv, tpu, puan, sozlu, yazili)
