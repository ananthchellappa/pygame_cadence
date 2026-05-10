from dataclasses import dataclass

from document import Document


@dataclass
class CommandContext:
    document: Document
