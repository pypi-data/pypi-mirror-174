"""
Portuguese Government-issued IDs:
  - NIF (Número de identificação fiscal)
  - CC (Número de Cartão de Cidadão)
"""

import re

from typing import Iterable

from stdnum.pt import nif, cc

from pii_data.types import PiiEnum, PiiEntity, DocumentChunk
from pii_extract.build import BasePiiTask


# regex for NIF & CC
_NIF_PATTERN = r"(?: PT \x20?)? (?: \d{3} \x20 \d{3} \x20 \d{3} | \d{9} )"
_CC_PATTERN = r"\d{8} \x20? \d \x20? [A-Z0-9]{2}\d"


class PortugueseNifCc(BasePiiTask):
    """
    Portuguese Government-issued NIF & CC numbers, recognize & validate
    """

    pii_name = "Portuguese NIF and CC numbers"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regexes
        self.nif = re.compile(_NIF_PATTERN, flags=re.X)
        self.cc = re.compile(_CC_PATTERN, flags=re.X)

    def find(self, chunk: DocumentChunk) -> Iterable[PiiEntity]:
        # NIF
        for item in self.nif.finditer(chunk.data):
            item_value = item.group()
            if nif.is_valid(item_value):
                yield PiiEntity(
                    PiiEnum.GOV_ID, item_value, chunk.id, item.start(),
                    country=self.country, subtype="Portuguese NIF"
                )
        # CC
        for item in self.cc.finditer(chunk.data):
            item_value = item.group()
            if cc.is_valid(item_value):
                yield PiiEntity(
                    PiiEnum.GOV_ID, item_value, chunk.id, item.start(),
                    country=self.country, subtype="Portuguese CC"
                )


# Task descriptor
PII_TASKS = [(PiiEnum.GOV_ID, PortugueseNifCc)]
