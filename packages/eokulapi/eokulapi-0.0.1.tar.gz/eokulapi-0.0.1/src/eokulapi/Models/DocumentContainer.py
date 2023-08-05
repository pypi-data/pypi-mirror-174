from dataclasses import dataclass
from typing import Optional

from eokulapi.Models import from_list
from eokulapi.Models.Document import Document


@dataclass
class DocumentContainer:
    belgeler: Optional[list[Document]]

    @staticmethod
    def from_dict(obj: dict) -> "DocumentContainer":
        liste = from_list(Document.from_dict, obj.get("TumBelgeler"))
        return DocumentContainer(liste)
