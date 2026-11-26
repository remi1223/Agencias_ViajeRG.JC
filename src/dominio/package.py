from datetime import date, datetime

class Package:
    def __init__(
        self,
        name: str,
        start_date: str | date,
        end_date: str | date,
        total_price: int | float,
        available_slots: int,
        status: bool = True,
        package_id: int | None = None,
    ):
        if not name or not name.strip():
            raise ValueError("El nombre del paquete no puede quedar vacío.")
        if len(name.strip()) > 150:
            raise ValueError("El nombre del paquete no puede superar los 150 caracteres.")

        if not start_date:
            raise ValueError("La fecha de inicio no puede quedar vacía.")
        parsed_start = self._parse_date(start_date, "fecha de inicio")

        if not end_date:
            raise ValueError("La fecha de término no puede quedar vacía.")
        parsed_end = self._parse_date(end_date, "fecha de término")

        if parsed_end < parsed_start:
            raise ValueError("La fecha de término no puede ser anterior a la fecha de inicio.")

        if total_price is None or total_price < 0:
            raise ValueError("El precio total no puede ser negativo.")

        if available_slots is None or available_slots < 0:
            raise ValueError("Los cupos disponibles no pueden ser negativos.")

        if not isinstance(status, bool):
            raise ValueError("El estado del paquete debe ser booleano (True/False).")

        self._package_id = package_id
        self._name = name.strip()
        self._start_date = parsed_start.strftime("%Y-%m-%d")
        self._end_date = parsed_end.strftime("%Y-%m-%d")
        self._total_price = total_price
        self._available_slots = available_slots
        self._status = status

    @staticmethod
    def _parse_date(value: str | date, field_label: str) -> date:
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"La {field_label} debe tener el formato AAAA-MM-DD.")
        raise ValueError(f"Formato de {field_label} no válido.")

    def show_data(self) -> str:
        status_text = "Disponible" if self._status else "No disponible"
        return (
            f"{self._package_id}-{self._name}-({self._start_date} a {self._end_date})-"
            f"${self._total_price}-Cupos: {self._available_slots}-{status_text}"
        )