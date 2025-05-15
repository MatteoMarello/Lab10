from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Arco:
    CCode1: int
    CCode2: int

    def __str__(self):
        return f"Confine tra {self.CCode1} e {self.CCode2}"
