from dataclasses import dataclass


@dataclass
class AvgMark:
    value: any
    aciklama: any
    aciklamadeger: any
    subeort: float | None

    @staticmethod
    def from_dict(obj: dict) -> "AvgMark":
        val = obj.get("value")
        ac = obj.get("description")
        ac_val = obj.get("description_value")
        avg_mark = obj.get("avg_mark")
        return AvgMark(val, ac, ac_val, avg_mark)
