from datetime import date
from dominio.user import User
from dominio.reservation import Reservation
from persistencia.reservationDAO import ReservationDAO
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


# =========================================================
# VISTAS ADMINISTRATIVAS (ROL: ADMIN)
# =========================================================

def create_reservation_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- REGISTRAR NUEVA RESERVA ---")
    try:
        user_id = read_int("ID del usuario: ")
        package_id = read_int("ID del paquete: ")
        reservation_date = input("Fecha de reserva (AAAA-MM-DD): ").strip()
        number_of_people = read_int("Cantidad de personas: ")
        total_amount = read_float("Monto total: ")

        new_reservation = Reservation(
            user_id=user_id,
            package_id=package_id,
            reservation_date=reservation_date,
            number_of_people=number_of_people,
            total_amount=total_amount,
            status=True,
        )

        new_id = reservation_dao.create_reservation(new_reservation)
        print(f"\nReserva registrada exitosamente con ID: {new_id}")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def list_reservations_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- LISTA DE TODAS LAS RESERVAS ---")
    try:
        reservations = reservation_dao.get_all_reservations()
        if not reservations:
            print("No hay reservas registradas en el sistema.")
        else:
            for res in reservations:
                print(res.show_data())

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_reservation_by_id_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- BUSCAR RESERVA POR ID ---")
    reservation_id = read_int("Ingrese el ID de la reserva: ")

    try:
        res = reservation_dao.get_reservation_by_id(reservation_id)
        if res:
            print(f"\nReserva encontrada: {res.show_data()}")
        else:
            print("\nNo se encontró ninguna reserva con ese ID.")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_reservations_by_user_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- BUSCAR RESERVAS POR USUARIO ---")
    user_id = read_int("Ingrese el ID del usuario: ")

    try:
        reservations = reservation_dao.get_reservations_by_user(user_id)
        if not reservations:
            print("\nEste usuario no tiene reservas registradas.")
        else:
            print(f"\nReservas del usuario {user_id}:")
            for res in reservations:
                print(res.show_data())

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def update_reservation_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- ACTUALIZAR RESERVA ---")
    reservation_id = read_int("Ingrese el ID de la reserva a modificar: ")

    try:
        existing = reservation_dao.get_reservation_by_id(reservation_id)
        if not existing:
            print("\nNo existe una reserva con ese ID.")
            return

        print(f"\nDatos actuales: {existing.show_data()}")
        print("(Presione Enter para mantener el valor actual)")

        user_str = input(f"Nuevo ID usuario [{existing._user_id}]: ").strip()
        pkg_str = input(f"Nuevo ID paquete [{existing._package_id}]: ").strip()
        date_str = input(f"Nueva fecha AAAA-MM-DD [{existing._reservation_date}]: ").strip()
        people_str = input(f"Nueva cantidad de personas [{existing._number_of_people}]: ").strip()
        amount_str = input(f"Nuevo monto total [{existing._total_amount}]: ").strip()
        current_status = "s" if existing._status else "n"
        status_str = input(f"¿Reserva activa? (s/n) [{current_status}]: ").strip().lower()

        updated_user = int(user_str) if user_str.isdigit() else existing._user_id
        updated_pkg = int(pkg_str) if pkg_str.isdigit() else existing._package_id
        updated_date = date_str if date_str else existing._reservation_date
        updated_people = int(people_str) if people_str.isdigit() else existing._number_of_people
        updated_amount = float(amount_str) if amount_str else existing._total_amount

        if status_str == "s":
            updated_status = True
        elif status_str == "n":
            updated_status = False
        else:
            updated_status = existing._status

        updated_reservation = Reservation(
            reservation_id=existing._reservation_id,
            user_id=updated_user,
            package_id=updated_pkg,
            reservation_date=updated_date,
            number_of_people=updated_people,
            total_amount=updated_amount,
            status=updated_status,
        )

        if reservation_dao.update_reservation(updated_reservation):
            print("\nReserva actualizada correctamente.")
        else:
            print("\nNo se realizaron cambios en la reserva.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def delete_reservation_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- ELIMINAR RESERVA ---")
    reservation_id = read_int("Ingrese el ID de la reserva a eliminar: ")

    try:
        res = reservation_dao.get_reservation_by_id(reservation_id)
        if not res:
            print("\nNo existe una reserva con ese ID.")
            return

        print(f"\nReserva a eliminar: {res.show_data()}")
        confirm = input("¿Está seguro de eliminar esta reserva? (s/n): ").strip().lower()

        if confirm == "s":
            if reservation_dao.delete_reservation(reservation_id):
                print("\nReserva eliminada correctamente.")
            else:
                print("\nNo se pudo eliminar la reserva.")
        else:
            print("\nOperación cancelada.")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_reservation_menu() -> None:
    reservation_dao = ReservationDAO()

    while True:
        clean_screen()
        print("===============================")
        print("     GESTIÓN DE RESERVAS")
        print("===============================")
        print("1. Crear reserva")
        print("2. Listar todas las reservas")
        print("3. Buscar reserva por ID")
        print("4. Buscar reservas por usuario")
        print("5. Actualizar reserva")
        print("6. Eliminar reserva")
        print("0. Volver / Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            create_reservation_view(reservation_dao)
        elif option == "2":
            list_reservations_view(reservation_dao)
        elif option == "3":
            search_reservation_by_id_view(reservation_dao)
        elif option == "4":
            search_reservations_by_user_view(reservation_dao)
        elif option == "5":
            update_reservation_view(reservation_dao)
        elif option == "6":
            delete_reservation_view(reservation_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()


# =========================================================
# VISTAS DE CLIENTE (ROL: USER)
# =========================================================

def contract_package_view(
    current_user: User,
    reservation_dao: ReservationDAO,
    package_dao: PackageDAO,
) -> None:
    clean_screen()
    print("--- CONTRATAR PAQUETE DE VIAJE ---")

    try:
        available_packages = package_dao.get_available_packages()
        if not available_packages:
            print("Por el momento no hay paquetes disponibles para contratar.")
            return

        print("Paquetes disponibles:")
        for pkg in available_packages:
            print(pkg.show_data())

        print("\n-----------------------------------")
        raw_pkg_id = input("Ingrese el ID del paquete que desea contratar: ").strip()
        if not raw_pkg_id.isdigit():
            print("\nError: Debe ingresar un ID de paquete numérico válido.")
            return

        package_id = int(raw_pkg_id)
        selected_pkg = package_dao.get_package_by_id(package_id)

        if not selected_pkg or not selected_pkg._status or selected_pkg._available_slots <= 0:
            print("\nError: El paquete seleccionado no existe o no tiene cupos disponibles.")
            return

        raw_people = input("Cantidad de personas que viajan: ").strip()
        if not raw_people.isdigit() or int(raw_people) <= 0:
            print("\nError: La cantidad de personas debe ser un entero mayor a 0.")
            return

        number_of_people = int(raw_people)

        if number_of_people > selected_pkg._available_slots:
            print(f"\nError: Solo quedan {selected_pkg._available_slots} cupos disponibles para este paquete.")
            return

        total_amount = selected_pkg._total_price * number_of_people
        today_str = date.today().strftime("%Y-%m-%d")

        print("\nResumen de contratación:")
        print(f"Paquete: {selected_pkg._name}")
        print(f"Personas: {number_of_people} x ${selected_pkg._total_price} = Total: ${total_amount}")
        confirm = input("¿Confirmar contratación? (s/n): ").strip().lower()

        if confirm != "s":
            print("\nContratación cancelada.")
            return

        new_reservation = Reservation(
            user_id=current_user._user_id,
            package_id=selected_pkg._package_id,
            reservation_date=today_str,
            number_of_people=number_of_people,
            total_amount=total_amount,
            status=True,
        )

        reservation_id = reservation_dao.create_reservation(new_reservation)

        selected_pkg._available_slots -= number_of_people
        if selected_pkg._available_slots == 0:
            selected_pkg._status = False
        package_dao.update_package(selected_pkg)

        print(f"\n¡Paquete contratado exitosamente! Código de reserva: {reservation_id}")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def my_reservations_view(current_user: User, reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print(f"--- MIS RESERVAS ({current_user._first_name}) ---")
    try:
        reservations = reservation_dao.get_reservations_by_user(current_user._user_id)
        if not reservations:
            print("Aún no tienes paquetes contratados.")
        else:
            for res in reservations:
                print(res.show_data())
    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_client_reservation_menu(current_user: User) -> None:
    reservation_dao = ReservationDAO()
    package_dao = PackageDAO()

    while True:
        clean_screen()
        print("===============================")
        print("   CONTRATACIÓN DE PAQUETES")
        print("===============================")
        print("1. Contratar un paquete")
        print("2. Ver mis paquetes contratados")
        print("0. Volver")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            contract_package_view(current_user, reservation_dao, package_dao)
        elif option == "2":
            my_reservations_view(current_user, reservation_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()


if __name__ == "__main__":
    run_reservation_menu()