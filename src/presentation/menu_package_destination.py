from dominio.package_destinations import PackageDestination
from persistencia.package_destinationDAO import PackageDestinationsDAO
from persistencia.packageDAO import PackageDAO
from persistencia.destinationDAO import DestinationDAO
from complementos.plugins import clean_screen, pause_and_clean


def read_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Error: Debe ingresar un número entero válido.")


def assign_destination_view(
    pkg_dest_dao: PackageDestinationsDAO,
    package_dao: PackageDAO,
    destination_dao: DestinationDAO,
) -> None:
    clean_screen()
    print("--- ASIGNAR DESTINO A PAQUETE ---")
    try:
        packages = package_dao.get_all_packages()
        destinations = destination_dao.get_all_destinations()

        if not packages or not destinations:
            print("Debe haber al menos un paquete y un destino creados antes de asociarlos.")
            return

        print("Paquetes disponibles:")
        for p in packages:
            print(f"  [{p._package_id}] {p._name}")

        print("\nDestinos disponibles:")
        for d in destinations:
            print(f"  [{d._destination_id}] {d._name}")

        print()
        package_id = read_int("ID del paquete: ")
        destination_id = read_int("ID del destino: ")

        relation = PackageDestination(
            package_id=package_id,
            destination_id=destination_id,
        )

        if pkg_dest_dao.add_destination_to_package(relation):
            pkg = package_dao.get_package_by_id(package_id)
            dest = destination_dao.get_destination_by_id(destination_id)
            pkg_label = pkg._name if pkg else f"ID {package_id}"
            dest_label = dest._name if dest else f"ID {destination_id}"
            print(f"\nDestino '{dest_label}' asignado exitosamente al paquete '{pkg_label}'.")
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
        relations = pkg_dest_dao.get_all_package_destinations_detailed()
        if not relations:
            print("No hay destinos asignados a ningún paquete todavía.")
        else:
            for rel in relations:
                print(
                    f"Paquete: {rel['package_name']} (ID: {rel['package_id']}) "
                    f"-> Destino: {rel['destination_name']} (ID: {rel['destination_id']})"
                )

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_destinations_by_package_view(
    pkg_dest_dao: PackageDestinationsDAO,
    package_dao: PackageDAO,
) -> None:
    clean_screen()
    print("--- CONSULTAR DESTINOS DE UN PAQUETE ---")
    package_id = read_int("Ingrese el ID del paquete: ")

    try:
        pkg = package_dao.get_package_by_id(package_id)
        if not pkg:
            print("\nNo existe un paquete con ese ID.")
            return

        destinos = pkg_dest_dao.get_destination_details_by_package(package_id)
        print(f"\nPaquete: {pkg._name}")
        if not destinos:
            print("Este paquete no tiene destinos asociados.")
        else:
            for d in destinos:
                desc = f" - {d._description}" if d._description else ""
                print(f"  -> Destino: {d._name}{desc}")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def remove_destination_from_package_view(pkg_dest_dao: PackageDestinationsDAO) -> None:
    clean_screen()
    print("--- QUITAR DESTINO DE UN PAQUETE ---")
    try:
        relations = pkg_dest_dao.get_all_package_destinations_detailed()
        if not relations:
            print("No hay asignaciones para eliminar.")
            return

        for rel in relations:
            print(
                f"Paquete: {rel['package_name']} (ID: {rel['package_id']}) "
                f"-> Destino: {rel['destination_name']} (ID: {rel['destination_id']})"
            )

        print()
        package_id = read_int("Ingrese el ID del paquete: ")
        destination_id = read_int("Ingrese el ID del destino a quitar: ")

        confirm = input("¿Desvincular este destino del paquete? (s/n): ").strip().lower()

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
    package_dao = PackageDAO()
    destination_dao = DestinationDAO()

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
            assign_destination_view(pkg_dest_dao, package_dao, destination_dao)
        elif option == "2":
            list_all_package_destinations_view(pkg_dest_dao)
        elif option == "3":
            search_destinations_by_package_view(pkg_dest_dao, package_dao)
        elif option == "4":
            remove_destination_from_package_view(pkg_dest_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()