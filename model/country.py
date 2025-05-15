from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Country:
    StateAbb: str
    CCode: int
    StateNme: str

    def __str__(self):
        return f"{self.StateNme} ({self.StateAbb})"
