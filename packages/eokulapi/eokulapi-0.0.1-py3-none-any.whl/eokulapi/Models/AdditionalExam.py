from dataclasses import dataclass
from typing import Optional

from eokulapi.Models import from_list, from_str


@dataclass
class AdditionalExam:
    name: Optional[str]
    basvurulistesi: list
    sonuclistesi: list
    yerlistesi: list

    @staticmethod
    def from_dict(obj: dict) -> "AdditionalExam":
        name = from_str(obj.get("SinavAdi"))
        basv = from_list(list, obj.get("sinavBasvuruListesi"))
        sonuc = from_list(list, obj.get("sinavSonucListesi"))
        yer = from_list(list, obj.get("sinavYeriListesi"))
        return AdditionalExam(name, basv, sonuc, yer)
