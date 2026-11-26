from datetime import date, datetime


class Reservation:
    def __init__(
        self,
        user_id: int,
        package_id: int,
        reservation_date: str | date,
        number_of_people: int,
        total_amount: int | float,
        status: bool = True,
        reservation_id: int | None = None,
    ):
        if user_id is None or user_id <= 0:
            raise ValueError("El ID de usuario no es válido.")

        if package_id is None or package_id <= 0:
            raise ValueError("El ID del paquete no es válido.")

        if not reservation_date:
            raise ValueError("La fecha de reserva no puede quedar vacía.")

        if isinstance(reservation_date, str):
            try:
                datetime.strptime(reservation_date.strip(), "%Y-%m-%d")
            except ValueError:
                raise ValueError("La fecha de reserva debe tener el formato AAAA-MM-DD.")

        if number_of_people is None or number_of_people <= 0:
            raise ValueError("La cantidad de personas debe ser mayor a cero.")

        if total_amount is None or total_amount < 0:
            raise ValueError("El monto total no puede ser negativo.")

        if not isinstance(status, bool):
            raise ValueError("El estado de la reserva debe ser booleano (True/False).")

        self._reservation_id = reservation_id
        self._user_id = user_id
        self._package_id = package_id
        self._reservation_date = str(reservation_date).strip()
        self._number_of_people = number_of_people
        self._total_amount = total_amount
        self._status = status

    def show_data(self) -> str:
        status_text = "Activa" if self._status else "Cancelada"
        return (
            f"{self._reservation_id}-{self._user_id}-{self._package_id}-"
            f"{self._reservation_date}-{self._number_of_people}-"
            f"${self._total_amount}-{status_text}"
        )