from dominio.country import Country
from persistencia.countryDAO import CountryDAO
from complementos.plugins import clean_screen, pause_and_clean


def read_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Error: Debe ingresar un número entero válido.")


def create_country_view(country_dao: CountryDAO) -> None:
    clean_screen()
    print("--- CREAR NUEVO PAÍS ---")
    try:
        name = input("Nombre del país: ").strip()
        new_country = Country(name=name)
        new_id = country_dao.create_country(new_country)
        print(f"\nPaís '{name}' creado exitosamente con ID: {new_id}")
    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def list_countries_view(country_dao: CountryDAO) -> None:
    clean_screen()
    print("--- LISTA DE PAÍSES ---")
    try:
        countries = country_dao.get_all_countries()
        if not countries:
            print("No hay países registrados.")
        else:
            for c in countries:
                print(c.show_data())
    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def update_country_view(country_dao: CountryDAO) -> None:
    clean_screen()
    print("--- ACTUALIZAR PAÍS ---")
    country_id = read_int("Ingrese el ID del país a modificar: ")
    try:
        existing = country_dao.get_country_by_id(country_id)
        if not existing:
            print("\nNo existe un país con ese ID.")
            return

        print(f"\nPaís actual: {existing.show_data()}")
        new_name = input(f"Nuevo nombre [{existing._name}]: ").strip() or existing._name

        updated = Country(country_id=existing._country_id, name=new_name)
        if country_dao.update_country(updated):
            print("\nPaís actualizado correctamente.")
        else:
            print("\nNo se realizaron cambios.")
    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def delete_country_view(country_dao: CountryDAO) -> None:
    clean_screen()
    print("--- ELIMINAR PAÍS ---")
    country_id = read_int("Ingrese el ID del país a eliminar: ")
    try:
        existing = country_dao.get_country_by_id(country_id)
        if not existing:
            print("\nNo existe un país con ese ID.")
            return

        print(f"\nPaís a eliminar: {existing.show_data()}")
        confirm = input("¿Está seguro de eliminar este país? (s/n): ").strip().lower()
        if confirm == "s":
            if country_dao.delete_country(country_id):
                print("\nPaís eliminado correctamente.")
            else:
                print("\nNo se pudo eliminar el país.")
        else:
            print("\nOperación cancelada.")
    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_country_menu() -> None:
    country_dao = CountryDAO()

    while True:
        clean_screen()
        print("======================================")
        print("          GESTIÓN DE PAÍSES")
        print("======================================")
        print("1. Crear país")
        print("2. Listar países")
        print("3. Actualizar país")
        print("4. Eliminar país")
        print("0. Volver / Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            create_country_view(country_dao)
        elif option == "2":
            list_countries_view(country_dao)
        elif option == "3":
            update_country_view(country_dao)
        elif option == "4":
            delete_country_view(country_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()