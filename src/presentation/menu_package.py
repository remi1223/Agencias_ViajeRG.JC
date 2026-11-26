from dominio.package import Package
from persistencia.packageDAO import PackageDAO
from complementos.plugins import clean_screen, pause_and_clean

def read_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Error: Debe ingresar un número entero válido.")


def read_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Error: Debe ingresar un monto numérico válido.")


def create_package_view(package_dao: PackageDAO) -> None:
    clean_screen()
    print("--- REGISTRAR NUEVO PAQUETE ---")
    try:
        name = input("Nombre del paquete: ").strip()
        start_date = input("Fecha de inicio (AAAA-MM-DD): ").strip()
        end_date = input("Fecha de término (AAAA-MM-DD): ").strip()
        total_price = read_float("Precio total: ")
        available_slots = read_int("Cupos disponibles: ")

        new_package = Package(
            name=name,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            available_slots=available_slots,
            status=True,
        )

        new_id = package_dao.create_package(new_package)
        print(f"\nPaquete registrado exitosamente con ID: {new_id}")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def list_packages_view(package_dao: PackageDAO, only_available: bool = False) -> None:
    clean_screen()
    title = "--- PAQUETES DISPONIBLES ---" if only_available else "--- LISTA DE PAQUETES ---"
    print(title)
    try:
        packages = (
            package_dao.get_available_packages()
            if only_available
            else package_dao.get_all_packages()
        )
        if not packages:
            print("No hay paquetes registrados para mostrar.")
        else:
            for pkg in packages:
                print(pkg.show_data())

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_package_view(package_dao: PackageDAO) -> None:
    clean_screen()
    print("--- BUSCAR PAQUETE ---")
    package_id = read_int("Ingrese el ID del paquete: ")

    try:
        pkg = package_dao.get_package_by_id(package_id)
        if pkg:
            print(f"\nPaquete encontrado: {pkg.show_data()}")
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

        print(f"\nDatos actuales: {existing.show_data()}")
        print("(Presione Enter para mantener el valor actual)")

        name_str = input(f"Nuevo nombre [{existing._name}]: ").strip()
        start_str = input(f"Nueva fecha inicio AAAA-MM-DD [{existing._start_date}]: ").strip()
        end_str = input(f"Nueva fecha término AAAA-MM-DD [{existing._end_date}]: ").strip()
        price_str = input(f"Nuevo precio total [{existing._total_price}]: ").strip()
        slots_str = input(f"Nuevos cupos disponibles [{existing._available_slots}]: ").strip()
        current_status = "s" if existing._status else "n"
        status_str = input(f"¿Paquete disponible? (s/n) [{current_status}]: ").strip().lower()

        updated_name = name_str if name_str else existing._name
        updated_start = start_str if start_str else existing._start_date
        updated_end = end_str if end_str else existing._end_date
        updated_price = float(price_str) if price_str else existing._total_price
        updated_slots = int(slots_str) if slots_str.isdigit() else existing._available_slots

        if status_str == "s":
            updated_status = True
        elif status_str == "n":
            updated_status = False
        else:
            updated_status = existing._status

        updated_package = Package(
            package_id=existing._package_id,
            name=updated_name,
            start_date=updated_start,
            end_date=updated_end,
            total_price=updated_price,
            available_slots=updated_slots,
            status=updated_status,
        )

        if package_dao.update_package(updated_package):
            print("\nPaquete actualizado correctamente.")
        else:
            print("\nNo se realizaron cambios en el paquete.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def delete_package_view(package_dao: PackageDAO) -> None:
    clean_screen()
    print("--- ELIMINAR PAQUETE ---")
    package_id = read_int("Ingrese el ID del paquete a eliminar: ")

    try:
        pkg = package_dao.get_package_by_id(package_id)
        if not pkg:
            print("\nNo existe un paquete con ese ID.")
            return

        print(f"\nPaquete a eliminar: {pkg.show_data()}")
        confirm = input("¿Está seguro de eliminar este paquete? (s/n): ").strip().lower()

        if confirm == "s":
            if package_dao.delete_package(package_id):
                print("\nPaquete eliminado correctamente.")
            else:
                print("\nNo se pudo eliminar el paquete.")
        else:
            print("\nOperación cancelada.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_package_menu() -> None:
    package_dao = PackageDAO()

    while True:
        clean_screen()
        print("===============================")
        print("     GESTIÓN DE PAQUETES")
        print("===============================")
        print("1. Crear paquete")
        print("2. Listar todos los paquetes")
        print("3. Listar paquetes disponibles")
        print("4. Buscar paquete por ID")
        print("5. Actualizar paquete")
        print("6. Eliminar paquete")
        print("0. Volver / Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            create_package_view(package_dao)
        elif option == "2":
            list_packages_view(package_dao, only_available=False)
        elif option == "3":
            list_packages_view(package_dao, only_available=True)
        elif option == "4":
            search_package_view(package_dao)
        elif option == "5":
            update_package_view(package_dao)
        elif option == "6":
            delete_package_view(package_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()


if __name__ == "__main__":
    run_package_menu()