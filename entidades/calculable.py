from abc import ABC, abstractmethod

class Calculable(ABC):
    """Contrato para objetos que calculan y actualizan un total."""
    @abstractmethod
    def calcular_total(self) -> None:
        raise NotImplementedError
