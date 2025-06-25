from dataclasses import dataclass


@dataclass
class Employee:
    name: str
    department: str
    rate: float
    hours: float

    @property
    def payout(self) -> float:
        return self.rate * self.hours
