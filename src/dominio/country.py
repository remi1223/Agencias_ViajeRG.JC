class Country:
    def __init__(self, name: str, country_id: int | None = None):
        if not name or not name.strip():
            raise ValueError("El nombre del país no puede quedar vacío.")

        self._country_id = country_id
        self._name = name.strip()

    def show_data(self) -> str:
        return f"{self._country_id} - {self._name}"