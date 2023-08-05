from dataclasses import dataclass
from datetime import datetime
from typing import Union

from eokulapi.Models import from_int, from_str, month_to_int


@dataclass
class ExamSchedule:
    isPast: bool
    date: datetime.date
    ders: str

    @staticmethod
    def from_dict(obj: dict) -> Union["ExamSchedule", None]:
        dtype = from_int(obj.get("Liste"))
        if dtype == 2:
            isPast = False
            gun = from_str(obj.get("Ders")).split()
            ders = from_str(obj.get("Gun"))
        elif dtype == 3:
            isPast = True
            gun = from_str(obj.get("Gun")).split()
            ders = from_str(obj.get("Ders"))
        else:
            return None
        date_str = f"{gun[0]:02};{month_to_int(gun[1]):02};{gun[2]:04}"
        date = datetime.strptime(date_str, "%d;%m;%Y")

        return ExamSchedule(isPast, date, ders)
