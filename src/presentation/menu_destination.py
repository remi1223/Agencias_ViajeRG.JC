from dominio.destination import Destination
from persistencia.destinationDAO import DestinationDAO
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


def create_destination_view(destination_dao: DestinationDAO) -> None:
    clean_screen()
    print("--- CREAR NUEVO DESTINO ---")
    try:
        name = input("Nombre del destino: ").strip()
        country_id = read_int("ID del país: ")
        description = input("Descripción (opcional, Enter para omitir): ").strip()
        base_cost = read_float("Costo base ($): ")
        status = read_bool("¿Destino activo? (s/n): ")

        new_destination = Destination(
            name=name,
            country_id=country_id,
            base_cost=base_cost,
            status=status,
            description=description if description else None,
        )

        new_id = destination_dao.create_destination(new_destination)
        print(f"\nDestino creado exitosamente con ID: {new_id}")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def list_destinations_view(destination_dao: DestinationDAO) -> None:
    clean_screen()
    print("--- LISTA DE DESTINOS ---")
    try:
        destinations = destination_dao.get_all_destinations()
        if not destinations:
            print("No hay destinos registrados.")
        else:
            for dest in destinations:
                print(dest.show_data())

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_destination_by_id_view(destination_dao: DestinationDAO) -> None:
    clean_screen()
    print("--- BUSCAR DESTINO POR ID ---")
    destination_id = read_int("Ingrese el ID del destino: ")

    try:
        dest = destination_dao.get_destination_by_id(destination_id)
        if dest:
            print("\nDestino encontrado:")
            print(dest.show_data())
        else:
            print("\nNo se encontró ningún destino con ese ID.")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def update_destination_view(destination_dao: DestinationDAO) -> None:
    clean_screen()
    print("--- ACTUALIZAR DESTINO ---")
    destination_id = read_int("Ingrese el ID del destino a modificar: ")

    try:
        existing = destination_dao.get_destination_by_id(destination_id)
        if not existing:
            print("\nNo existe un destino con ese ID.")
            return

        print(f"\nDestino actual: {existing.show_data()}")
        print("Presione Enter para mantener el valor actual.\n")

        new_name = input(f"Nuevo nombre [{existing._name}]: ").strip() or existing._name

        raw_country = input(f"Nuevo ID de país [{existing._country_id}]: ").strip()
        new_country_id = int(raw_country) if raw_country.isdigit() else existing._country_id

        current_desc = existing._description if existing._description else ""
        raw_desc = input(f"Nueva descripción [{current_desc}]: ").strip()
        new_desc = raw_desc if raw_desc else existing._description

        raw_cost = input(f"Nuevo costo base [{existing._base_cost}]: ").strip().replace(",", ".")
        new_cost = float(raw_cost) if raw_cost else existing._base_cost

        raw_status = input(
            f"¿Activo? (s/n) [{'s' if existing._status else 'n'}]: "
        ).strip().lower()
        if raw_status in ("s", "si", "sí", "1", "true"):
            new_status = True
        elif raw_status in ("n", "no", "0", "false"):
            new_status = False
        else:
            new_status = existing._status

        updated_dest = Destination(
            destination_id=existing._destination_id,
            name=new_name,
            country_id=new_country_id,
            base_cost=new_cost,
            status=new_status,
            description=new_desc,
        )

        if destination_dao.update_destination(updated_dest):
            print("\nDestino actualizado correctamente.")
        else:
            print("\nNo se realizaron cambios.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def delete_destination_view(destination_dao: DestinationDAO) -> None:
    clean_screen()
    print("--- ELIMINAR DESTINO ---")
    destination_id = read_int("Ingrese el ID del destino a eliminar: ")

    try:
        existing = destination_dao.get_destination_by_id(destination_id)
        if not existing:
            print("\nNo existe un destino con ese ID.")
            return

        print(f"\nDestino a eliminar: {existing.show_data()}")
        confirm = input("¿Está seguro de eliminar este destino? (s/n): ").strip().lower()

        if confirm == "s":
            if destination_dao.delete_destination(destination_id):
                print("\nDestino eliminado correctamente.")
            else:
                print("\nNo se pudo eliminar el destino.")
        else:
            print("\nOperación cancelada.")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_destination_menu() -> None:
    destination_dao = DestinationDAO()

    while True:
        clean_screen()
        print("======================================")
        print("         GESTIÓN DE DESTINOS")
        print("======================================")
        print("1. Crear destino")
        print("2. Listar destinos")
        print("3. Buscar destino por ID")
        print("4. Actualizar destino")
        print("5. Eliminar destino")
        print("0. Volver / Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            create_destination_view(destination_dao)
        elif option == "2":
            list_destinations_view(destination_dao)
        elif option == "3":
            search_destination_by_id_view(destination_dao)
        elif option == "4":
            update_destination_view(destination_dao)
        elif option == "5":
            delete_destination_view(destination_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()


if __name__ == "__main__":
    run_destination_menu()