class PackageDestination:
    def __init__(self, package_id: int, destination_id: int):
        if not isinstance(package_id, int) or package_id <= 0:
            raise ValueError("El ID del paquete debe ser un entero positivo.")
        if not isinstance(destination_id, int) or destination_id <= 0:
            raise ValueError("El ID del destino debe ser un entero positivo.")

        self._package_id = package_id
        self._destination_id = destination_id

    def show_data(self) -> str:
        return f"Paquete ID: {self._package_id} <-> Destino ID: {self._destination_id}"