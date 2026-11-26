from dominio.package import Package
from persistencia.packageDAO import PackageDAO
from persistencia.package_destinationDAO import PackageDestinationsDAO
from complementos.plugins import clean_screen, pause_and_clean


def read_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Error: Debe ingresar un número entero válido.")


def read_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip().replace(",", ".")
        try:
            number = float(value)
            if number < 0:
                print("Error: El monto no puede ser negativo.")
                continue
            return number
        except ValueError:
            print("Error: Debe ingresar un número válido.")


def read_bool(prompt: str) -> bool:
    while True:
        value = input(prompt).strip().lower()
        if value in ("s", "si", "sí", "1", "true"):
            return True
        if value in ("n", "no", "0", "false"):
            return False
        print("Error: Responda 's' para sí o 'n' para no.")


def _print_destinations_for_package(pkg_dest_dao: PackageDestinationsDAO, package_id: int) -> None:
    destinos = pkg_dest_dao.get_destination_details_by_package(package_id)
    if destinos:
        nombres = ", ".join(d._name for d in destinos)
        print(f"   -> Destinos incluidos: {nombres}")
    else:
        print("   -> Destinos incluidos: Sin destinos asignados")


def create_package_view(package_dao: PackageDAO) -> None:
    clean_screen()
    print("--- CREAR NUEVO PAQUETE ---")
    try:
        name = input("Nombre del paquete: ").strip()
        start_date = input("Fecha de inicio (YYYY-MM-DD): ").strip()
        end_date = input("Fecha de término (YYYY-MM-DD): ").strip()
        total_price = read_float("Precio total ($): ")
        available_slots = read_int("Cupos disponibles: ")
        status = read_bool("¿Paquete activo? (s/n): ")

        new_package = Package(
            name=name,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            available_slots=available_slots,
            status=status,
        )

        new_id = package_dao.create_package(new_package)
        print(f"\nPaquete creado exitosamente con ID: {new_id}")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def list_packages_view(package_dao: PackageDAO, only_available: bool = False) -> None:
    clean_screen()
    title = "--- PAQUETES DISPONIBLES ---" if only_available else "--- LISTA DE PAQUETES ---"
    print(title)
    pkg_dest_dao = PackageDestinationsDAO()

    try:
        packages = (
            package_dao.get_available_packages()
            if only_available
            else package_dao.get_all_packages()
        )
        if not packages:
            print("No hay paquetes registrados.")
        else:
            for pkg in packages:
                print(pkg.show_data())
                _print_destinations_for_package(pkg_dest_dao, pkg._package_id)
                print("-" * 55)

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_package_by_id_view(package_dao: PackageDAO) -> None:
    clean_screen()
    print("--- BUSCAR PAQUETE POR ID ---")
    package_id = read_int("Ingrese el ID del paquete: ")
    pkg_dest_dao = PackageDestinationsDAO()

    try:
        pkg = package_dao.get_package_by_id(package_id)
        if pkg:
            print("\nPaquete encontrado:")
            print(pkg.show_data())
            _print_destinations_for_package(pkg_dest_dao, pkg._package_id)
        else:
            print("\nNo se encontró ningún paquete con ese ID.")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def update_package_view(package_dao: PackageDAO) -> None:
    clean_screen()
    print("--- ACTUALIZAR PAQUETE ---")
    package_id = read_int("Ingrese el ID del paquete a modificar: ")

    try:
        existing = package_dao.get_package_by_id(package_id)
        if not existing:
            print("\nNo existe un paquete con ese ID.")
            return

        print(f"\nPaquete actual: {existing.show_data()}")
        print("Presione Enter para mantener el valor actual.\n")

        new_name = input(f"Nuevo nombre [{existing._name}]: ").strip() or existing._name
        new_start = input(f"Nueva fecha inicio [{existing._start_date}]: ").strip() or str(existing._start_date)
        new_end = input(f"Nueva fecha término [{existing._end_date}]: ").strip() or str(existing._end_date)

        raw_price = input(f"Nuevo precio [{existing._total_price}]: ").strip().replace(",", ".")
        new_price = float(raw_price) if raw_price else existing._total_price

        raw_slots = input(f"Nuevos cupos [{existing._available_slots}]: ").strip()
        new_slots = int(raw_slots) if raw_slots.isdigit() else existing._available_slots

        raw_status = input(
            f"¿Activo? (s/n) [{'s' if existing._status else 'n'}]: "
        ).strip().lower()
        if raw_status in ("s", "si", "sí", "1", "true"):
            new_status = True
        elif raw_status in ("n", "no", "0", "false"):
            new_status = False
        else:
            new_status = existing._status

        updated_pkg = Package(
            package_id=existing._package_id,
            name=new_name,
            start_date=new_start,
            end_date=new_end,
            total_price=new_price,
            available_slots=new_slots,
            status=new_status,
        )

        if package_dao.update_package(updated_pkg):
            print("\nPaquete actualizado correctamente.")
        else:
            print("\nNo se realizaron cambios.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def delete_package_view(package_dao: PackageDAO) -> None:
    clean_screen()
    print("--- ELIMINAR PAQUETE ---")
    package_id = read_int("Ingrese el ID del paquete a eliminar: ")

    try:
        existing = package_dao.get_package_by_id(package_id)
        if not existing:
            print("\nNo existe un paquete con ese ID.")
            return

        print(f"\nPaquete a eliminar: {existing.show_data()}")
        confirm = input("¿Está seguro de eliminar este paquete? (s/n): ").strip().lower()

        if confirm == "s":
            if package_dao.delete_package(package_id):
                print("\nPaquete eliminado correctamente.")
            else:
                print("\nNo se pudo eliminar el paquete.")
        else:
            print("\nOperación cancelada.")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_package_menu() -> None:
    package_dao = PackageDAO()

    while True:
        clean_screen()
        print("======================================")
        print("         GESTIÓN DE PAQUETES")
        print("======================================")
        print("1. Crear paquete")
        print("2. Listar paquetes")
        print("3. Buscar paquete por ID")
        print("4. Actualizar paquete")
        print("5. Eliminar paquete")
        print("0. Volver / Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            create_package_view(package_dao)
        elif option == "2":
            list_packages_view(package_dao)
        elif option == "3":
            search_package_by_id_view(package_dao)
        elif option == "4":
            update_package_view(package_dao)
        elif option == "5":
            delete_package_view(package_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()