from dataclasses import dataclass
from typing import Optional

from eokulapi.Models import from_list
from eokulapi.Models.ExamSchedule import ExamSchedule


@dataclass
class ExamScheduleContainer:
    sinavtarihleri: Optional[list[ExamSchedule]]

    @staticmethod
    def from_dict(obj: dict) -> "ExamScheduleContainer":
        tarihler = from_list(ExamSchedule.from_dict, obj.get("SinavTarihleriListesi"))
        tarihler = list(filter(lambda item: item is not None, tarihler))

        return ExamScheduleContainer(tarihler)
