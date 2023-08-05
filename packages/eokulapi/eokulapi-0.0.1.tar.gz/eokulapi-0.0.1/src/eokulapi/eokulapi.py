import logging
import random
import secrets
from base64 import b64decode

import requests

from eokulapi.Models.AbsenteeismContainer import AbsenteeismContainer
from eokulapi.Models.AdditionalExam import AdditionalExam
from eokulapi.Models.AvgMarkContainer import AvgMarkContainer
from eokulapi.Models.DocumentContainer import DocumentContainer
from eokulapi.Models.EndtermMarkContainer import EndtermMarkContainer
from eokulapi.Models.EokulException import EokulException
from eokulapi.Models.EokulStudent import EokulStudent
from eokulapi.Models.ExamScheduleContainer import ExamScheduleContainer
from eokulapi.Models.LessonSchedule import LessonSchedule
from eokulapi.Models.MarkContainer import MarkContainer
from eokulapi.Models.Responsibility import Responsibility
from eokulapi.Models.Transfer import Transfer

api = "https://e-okul.meb.gov.tr/mobileokulv2"
api_fixed_password = "2^Wd@FJhzWyaf&CE;47RY$.z>=.7~E>w"
user_agent = "Dart/2.8 (dart:io)"
app_version = "2.0.12"

routes = {
    "register": "/CihazKayit",
    "add_student": "/OgrenciEkle",
    "login_student": "/OgrenciGiris",
    "marks": "/NotBilgileri",
    "absenteeism": "/Devamsizlik",
    "lesson_schedule": "/DersProgrami",
    "exam_schedule": "/SinavTarihleri",
    "avg_marks": "/SubeYaziliOrtalamalari",
    "endterm_marks": "/YilSonuNotlari",
    "transfer": "/NakilBilgisi",
    "responsibibility": "/SorumlulukOys",
    "documents": "/AldigiBelgeler",
    "additional_exam": "/SinavBilgileri",
}


class EokulAPI:
    def __init__(self, uid=None) -> None:
        if not uid:
            uid = self.__uid_generator()
        self.uid = uid
        self.gid = None
        self.students: list[EokulStudent] = []
        self.session = requests.session()
        self.session.hooks = dict(response=self.__hook)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)
        self.register()

    def register(self) -> dict:
        resp = self.session.post(
            url=api + routes["register"],
            headers=self.__header_generator(),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "p": app_version,
                "pid": "",
            },
        )

        self.gid = resp.json()["GID"]
        return resp.json()

    def add_student(self, tckn: str, okulno: int, kimliktipi: bool, **kimlikbilgileri) -> dict:
        if kimliktipi == True:
            kimlikbilgileri["cilt"] = "yeniKimlik"
            kimlikbilgileri["aile"] = "yeniKimlik"
        else:
            kimlikbilgileri["seri"] = "eskiKimlik"

        pushid = self.__pushid_generator()
        resp = self.session.post(
            url=api + routes["add_student"],
            headers=self.__header_generator(),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
                "tckn": tckn,
                "okulNo": str(okulno),
                "aileSiraNo": kimlikbilgileri["aile"],
                "ciltNo": kimlikbilgileri["cilt"],
                "seriNo": kimlikbilgileri["seri"],
                "kimlikTipi": str(int(kimliktipi)),
                "ip": "1.1.1.1",  # bu ne acaba
                "push_id": pushid,
            },
        )

        return resp.json()

    def update_student_list(self) -> list:
        data = self.register()
        self.students.clear()
        for student in data["OgrenciListesi"]:
            login = self.__student_login(student["Tckn"])
            self.students.append(
                EokulStudent(
                    student["Tckn"],
                    student["AdSoyad"],
                    b64decode(student["Fotograf"]),
                    login["OgrenciToken"],
                    login["Sinif"],
                    login["SinifNo"],
                    login["Numarasi"],
                )
            )
        return self.students

    def update_student_data(self, student: EokulStudent) -> None:
        self.__update_marks(student)
        self.__update_absenteeism(student)
        self.__update_lesson_schedule(student)
        self.__update_exam_schedule(student)
        self.__update_class_exam_average(student)
        self.__update_endterm_marks(student)
        self.__update_transfer(student)
        self.__update_responsibility(student)
        self.__update_documents(student)
        self.__update_additional_exams(student)

    def __update_marks(self, student: EokulStudent) -> None:
        resp = self.session.post(
            url=api + routes["marks"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.marks = MarkContainer.from_dict(resp.json())
        return resp.json()

    def __update_absenteeism(self, student: EokulStudent) -> None:
        resp = self.session.post(
            url=api + routes["absenteeism"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.absenteeism = AbsenteeismContainer.from_dict(resp.json())
        return resp.json()

    def __update_lesson_schedule(self, student: EokulStudent) -> None:
        resp = self.session.post(
            url=api + routes["lesson_schedule"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.lesson_schedule = LessonSchedule.from_dict(resp.json())
        return resp.json()

    def __update_exam_schedule(self, student: EokulStudent) -> None:
        resp = self.session.post(
            url=api + routes["exam_schedule"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.exam_schedule = ExamScheduleContainer.from_dict(resp.json())
        return resp.json()

    def __update_class_exam_average(self, student: EokulStudent) -> None:
        resp = self.session.post(
            url=api + routes["avg_marks"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.class_exam_average = AvgMarkContainer.from_dict(resp.json())
        return resp.json()

    def __update_endterm_marks(self, student: EokulStudent) -> None:
        resp = self.session.post(
            url=api + routes["endterm_marks"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.endterm_marks = EndtermMarkContainer.from_dict(resp.json())
        return resp.json()

    def __update_transfer(self, student: EokulStudent) -> None:
        return "not implemented"
        resp = self.session.post(
            url=api + routes["transfer"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.transfer = Transfer.from_dict(resp.json())
        return resp.json()

    def __update_responsibility(self, student: EokulStudent) -> None:
        return "not implemented"
        resp = self.session.post(
            url=api + routes["responsibility"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.responsibility = Responsibility.from_dict(resp.json())
        return resp.json()

    def __update_documents(self, student: EokulStudent) -> None:
        resp = self.session.post(
            url=api + routes["documents"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
            },
        )
        student.documents = DocumentContainer.from_dict(resp.json())
        return resp.json()

    def __update_additional_exams(self, student: EokulStudent) -> None:
        resp = self.session.post(
            url=api + routes["additional_exam"],
            headers=self.__header_generator(student.token),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
                "sinifNo": str(student.sinifno),
            },
        )
        student.additionalexams = AdditionalExam.from_dict(resp.json())
        return resp.json()

    def __student_login(self, tckn: int) -> dict:
        resp = self.session.post(
            url=api + routes["login_student"],
            headers=self.__header_generator(),
            json={
                "sifre": api_fixed_password,
                "uid": self.uid,
                "gid": self.gid,
                "tckn": str(tckn),
                "mobile_platform": "android",
            },
        )
        return resp.json()

    def __pushid_generator(self) -> str:
        raise EokulException("we dont know how pushid generated")

    def __header_generator(self, bearer: str = None) -> dict[str, str]:
        header = {
            "User-Agent": user_agent,
            "Content-Type": "application/json; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Host": "e-okul.meb.gov.tr",
            "Connection": "close",
        }
        if bearer:
            header["Authorization"] = f"Bearer {bearer}"
        return header

    def __uid_generator() -> str:
        rand = random.SystemRandom()
        uid = f"{secrets.token_hex(16)}-{rand.randint(0,1000000000):09d}-{rand.randint(0,1000000000):09d}-{rand.randint(0,1000000):06d}"
        return uid

    def __hook(self, resp, *args, **kwargs):
        if resp.status_code != 200 or resp.json()["DurumKodu"] != 200:
            raise EokulException(f"{resp},{resp.json()}")
