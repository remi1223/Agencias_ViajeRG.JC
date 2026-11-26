from dominio.package_destinations import PackageDestination
from persistencia.package_destinationDAO import PackageDestinationsDAO
from complementos.plugins import clean_screen, pause_and_clean


def read_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Error: Debe ingresar un número entero válido.")


def assign_destination_view(pkg_dest_dao: PackageDestinationsDAO) -> None:
    clean_screen()
    print("--- ASIGNAR DESTINO A PAQUETE ---")
    try:
        package_id = read_int("ID del paquete: ")
        destination_id = read_int("ID del destino: ")

        relation = PackageDestination(
            package_id=package_id,
            destination_id=destination_id,
        )

        if pkg_dest_dao.add_destination_to_package(relation):
            print(f"\nDestino {destination_id} asignado exitosamente al paquete {package_id}.")
        else:
            print("\nNo se pudo realizar la asignación.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def list_all_package_destinations_view(pkg_dest_dao: PackageDestinationsDAO) -> None:
    clean_screen()
    print("--- DESTINOS ASIGNADOS A PAQUETES ---")
    try:
        relations = pkg_dest_dao.get_all_package_destinations()
        if not relations:
            print("No hay destinos asignados a ningún paquete todavía.")
        else:
            for rel in relations:
                print(rel.show_data())

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_destinations_by_package_view(pkg_dest_dao: PackageDestinationsDAO) -> None:
    clean_screen()
    print("--- CONSULTAR DESTINOS DE UN PAQUETE ---")
    package_id = read_int("Ingrese el ID del paquete: ")

    try:
        relations = pkg_dest_dao.get_destinations_by_package(package_id)
        if not relations:
            print("\nEste paquete no tiene destinos asociados.")
        else:
            print(f"\nDestinos del paquete {package_id}:")
            for rel in relations:
                print(rel.show_data())

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def remove_destination_from_package_view(pkg_dest_dao: PackageDestinationsDAO) -> None:
    clean_screen()
    print("--- QUITAR DESTINO DE UN PAQUETE ---")
    package_id = read_int("Ingrese el ID del paquete: ")
    destination_id = read_int("Ingrese el ID del destino a quitar: ")

    try:
        confirm = input(
            f"¿Desvincular el destino {destination_id} del paquete {package_id}? (s/n): "
        ).strip().lower()

        if confirm == "s":
            if pkg_dest_dao.remove_destination_from_package(package_id, destination_id):
                print("\nDestino desvinculado correctamente del paquete.")
            else:
                print("\nNo se encontró esa asociación paquete-destino.")
        else:
            print("\nOperación cancelada.")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_package_destinations_menu() -> None:
    pkg_dest_dao = PackageDestinationsDAO()

    while True:
        clean_screen()
        print("======================================")
        print("   GESTIÓN DE DESTINOS POR PAQUETE")
        print("======================================")
        print("1. Asignar destino a un paquete")
        print("2. Listar todas las asignaciones")
        print("3. Ver destinos de un paquete por ID")
        print("4. Quitar destino de un paquete")
        print("0. Volver / Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            assign_destination_view(pkg_dest_dao)
        elif option == "2":
            list_all_package_destinations_view(pkg_dest_dao)
        elif option == "3":
            search_destinations_by_package_view(pkg_dest_dao)
        elif option == "4":
            remove_destination_from_package_view(pkg_dest_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()


if __name__ == "__main__":
    run_package_destinations_menu()