from dataclasses import dataclass
from typing import Optional

from eokulapi.Models.AbsenteeismContainer import AbsenteeismContainer
from eokulapi.Models.AdditionalExam import AdditionalExam
from eokulapi.Models.AvgMarkContainer import AvgMarkContainer
from eokulapi.Models.DocumentContainer import DocumentContainer
from eokulapi.Models.EndtermMarkContainer import EndtermMarkContainer
from eokulapi.Models.ExamScheduleContainer import ExamScheduleContainer
from eokulapi.Models.LessonSchedule import LessonSchedule
from eokulapi.Models.MarkContainer import MarkContainer
from eokulapi.Models.Responsibility import Responsibility
from eokulapi.Models.Transfer import Transfer


@dataclass
class EokulStudent:
    tckn: int
    adsoyad: str
    photo: bytes
    token: str
    sinif: str
    sinifno: int
    no: int
    photo: bytes
    marks: Optional[MarkContainer] = None
    absenteeism: Optional[AbsenteeismContainer] = None
    lesson_schedule: Optional[LessonSchedule] = None
    exam_schedule: Optional[ExamScheduleContainer] = None
    class_exam_average: Optional[AvgMarkContainer] = None
    endterm_marks: Optional[EndtermMarkContainer] = None
    transfer: Optional[Transfer] = None
    responsibility: Optional[Responsibility] = None
    documents: Optional[DocumentContainer] = None
    additionalexams: Optional[AdditionalExam] = None
