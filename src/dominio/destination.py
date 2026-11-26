class Destination:
    def __init__(
        self,
        name: str,
        country_id: int,
        base_cost: float,
        status: bool = True,
        description: str | None = None,
        destination_id: int | None = None,
    ):
        if not name or not name.strip():
            raise ValueError("El nombre del destino no puede quedar vacío.")
        if not isinstance(country_id, int) or country_id <= 0:
            raise ValueError("El ID del país debe ser un entero positivo.")
        if base_cost < 0:
            raise ValueError("El costo base no puede ser negativo.")

        self._destination_id = destination_id
        self._name = name.strip()
        self._country_id = country_id
        self._description = description.strip() if description else None
        self._base_cost = float(base_cost)
        self._status = bool(status)

    def show_data(self) -> str:
        estado = "Activo" if self._status else "Inactivo"
        desc = self._description if self._description else "Sin descripción"
        return (
            f"{self._destination_id} - {self._name} | País ID: {self._country_id} | "
            f"Costo base: ${self._base_cost:,.0f} | {estado} ({desc})"
        )