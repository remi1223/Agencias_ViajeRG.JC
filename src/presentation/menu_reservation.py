from datetime import date
from dominio.user import User
from dominio.reservation import Reservation
from persistencia.reservationDAO import ReservationDAO
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


def _print_package_destinations(pkg_dest_dao: PackageDestinationsDAO, package_id: int) -> None:
    destinos = pkg_dest_dao.get_destination_details_by_package(package_id)
    if destinos:
        for dest in destinos:
            desc = f" - {dest._description}" if dest._description else ""
            print(f"   -> Destino: {dest._name}{desc}")
    else:
        print("   -> Destinos incluidos: Por definir")


# =========================================================
# VISTAS EXCLUSIVAS PARA CLIENTE (ROL: user)
# =========================================================

def contract_package_view(
    current_user: User,
    reservation_dao: ReservationDAO,
    package_dao: PackageDAO,
    pkg_dest_dao: PackageDestinationsDAO,
) -> None:
    clean_screen()
    print("--- CONTRATAR PAQUETE DE VIAJE ---")

    try:
        available_packages = package_dao.get_available_packages()
        if not available_packages:
            print("Por el momento no hay paquetes disponibles para contratar.")
            return

        print("Paquetes disponibles:\n")
        for pkg in available_packages:
            print(pkg.show_data())
            _print_package_destinations(pkg_dest_dao, pkg._package_id)
            print("-" * 55)

        raw_pkg_id = input("\nIngrese el ID del paquete que desea contratar: ").strip()
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
        _print_package_destinations(pkg_dest_dao, selected_pkg._package_id)
        print(f"Personas: {number_of_people} x ${selected_pkg._total_price:,.0f} = Total: ${total_amount:,.0f}")
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


def my_reservations_view(
    current_user: User,
    reservation_dao: ReservationDAO,
    pkg_dest_dao: PackageDestinationsDAO,
) -> None:
    clean_screen()
    print(f"--- MIS RESERVAS ({current_user._first_name}) ---\n")
    package_dao = PackageDAO()
    try:
        reservations = reservation_dao.get_reservations_by_user(current_user._user_id)
        if not reservations:
            print("Aún no tienes paquetes contratados.")
        else:
            for res in reservations:
                pkg = package_dao.get_package_by_id(res._package_id)
                pkg_name = pkg._name if pkg else "Paquete no disponible"
                estado = "Confirmada" if res._status else "Cancelada"
                print(
                    f"Reserva #{res._reservation_id} | Paquete: {pkg_name} | "
                    f"Fecha: {res._reservation_date} | Personas: {res._number_of_people} | "
                    f"Total: ${res._total_amount:,.0f} | {estado}"
                )
                _print_package_destinations(pkg_dest_dao, res._package_id)
                print("-" * 55)
    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_client_reservation_menu(current_user: User) -> None:
    reservation_dao = ReservationDAO()
    package_dao = PackageDAO()
    pkg_dest_dao = PackageDestinationsDAO()

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
            contract_package_view(current_user, reservation_dao, package_dao, pkg_dest_dao)
        elif option == "2":
            my_reservations_view(current_user, reservation_dao, pkg_dest_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()


# =========================================================
# VISTAS ADMINISTRATIVAS (ROL: admin)
# =========================================================

def create_reservation_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- CREAR NUEVA RESERVA ---")
    try:
        user_id = read_int("ID del usuario: ")
        package_id = read_int("ID del paquete: ")
        reservation_date = input("Fecha de reserva (YYYY-MM-DD): ").strip()
        number_of_people = read_int("Cantidad de personas: ")
        total_amount = read_float("Monto total ($): ")
        status = read_bool("¿Reserva activa/confirmada? (s/n): ")

        new_reservation = Reservation(
            user_id=user_id,
            package_id=package_id,
            reservation_date=reservation_date,
            number_of_people=number_of_people,
            total_amount=total_amount,
            status=status,
        )

        new_id = reservation_dao.create_reservation(new_reservation)
        print(f"\nReserva creada exitosamente con ID: {new_id}")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def list_reservations_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- LISTA DE RESERVAS ---\n")
    package_dao = PackageDAO()
    pkg_dest_dao = PackageDestinationsDAO()
    try:
        reservations = reservation_dao.get_all_reservations()
        if not reservations:
            print("No hay reservas registradas.")
        else:
            for res in reservations:
                pkg = package_dao.get_package_by_id(res._package_id)
                pkg_name = pkg._name if pkg else f"Paquete ID {res._package_id}"
                estado = "Activa" if res._status else "Cancelada"
                print(
                    f"Reserva #{res._reservation_id} | Usuario ID: {res._user_id} | "
                    f"Paquete: {pkg_name} | Fecha: {res._reservation_date} | "
                    f"Personas: {res._number_of_people} | Total: ${res._total_amount:,.0f} | {estado}"
                )
                _print_package_destinations(pkg_dest_dao, res._package_id)
                print("-" * 55)

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_reservation_by_id_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- BUSCAR RESERVA POR ID ---")
    reservation_id = read_int("Ingrese el ID de la reserva: ")
    package_dao = PackageDAO()
    pkg_dest_dao = PackageDestinationsDAO()

    try:
        res = reservation_dao.get_reservation_by_id(reservation_id)
        if res:
            pkg = package_dao.get_package_by_id(res._package_id)
            pkg_name = pkg._name if pkg else f"Paquete ID {res._package_id}"
            estado = "Activa" if res._status else "Cancelada"
            print("\nReserva encontrada:")
            print(
                f"Reserva #{res._reservation_id} | Usuario ID: {res._user_id} | "
                f"Paquete: {pkg_name} | Fecha: {res._reservation_date} | "
                f"Personas: {res._number_of_people} | Total: ${res._total_amount:,.0f} | {estado}"
            )
            _print_package_destinations(pkg_dest_dao, res._package_id)
        else:
            print("\nNo se encontró ninguna reserva con ese ID.")

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

        print(f"\nReserva actual: {existing.show_data()}")
        print("Presione Enter para mantener el valor actual.\n")

        raw_user = input(f"Nuevo ID de usuario [{existing._user_id}]: ").strip()
        new_user_id = int(raw_user) if raw_user.isdigit() else existing._user_id

        raw_pkg = input(f"Nuevo ID de paquete [{existing._package_id}]: ").strip()
        new_pkg_id = int(raw_pkg) if raw_pkg.isdigit() else existing._package_id

        new_date = input(f"Nueva fecha [{existing._reservation_date}]: ").strip() or existing._reservation_date

        raw_people = input(f"Nueva cantidad de personas [{existing._number_of_people}]: ").strip()
        new_people = int(raw_people) if raw_people.isdigit() else existing._number_of_people

        raw_amount = input(f"Nuevo monto total [{existing._total_amount}]: ").strip().replace(",", ".")
        new_amount = float(raw_amount) if raw_amount else existing._total_amount

        raw_status = input(
            f"¿Activa? (s/n) [{'s' if existing._status else 'n'}]: "
        ).strip().lower()
        if raw_status in ("s", "si", "sí", "1", "true"):
            new_status = True
        elif raw_status in ("n", "no", "0", "false"):
            new_status = False
        else:
            new_status = existing._status

        updated_res = Reservation(
            reservation_id=existing._reservation_id,
            user_id=new_user_id,
            package_id=new_pkg_id,
            reservation_date=new_date,
            number_of_people=new_people,
            total_amount=new_amount,
            status=new_status,
        )

        if reservation_dao.update_reservation(updated_res):
            print("\nReserva actualizada correctamente.")
        else:
            print("\nNo se realizaron cambios.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def delete_reservation_view(reservation_dao: ReservationDAO) -> None:
    clean_screen()
    print("--- ELIMINAR RESERVA ---")
    reservation_id = read_int("Ingrese el ID de la reserva a eliminar: ")

    try:
        existing = reservation_dao.get_reservation_by_id(reservation_id)
        if not existing:
            print("\nNo existe una reserva con ese ID.")
            return

        print(f"\nReserva a eliminar: {existing.show_data()}")
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
        print("======================================")
        print("         GESTIÓN DE RESERVAS")
        print("======================================")
        print("1. Crear reserva")
        print("2. Listar reservas")
        print("3. Buscar reserva por ID")
        print("4. Actualizar reserva")
        print("5. Eliminar reserva")
        print("0. Volver / Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            create_reservation_view(reservation_dao)
        elif option == "2":
            list_reservations_view(reservation_dao)
        elif option == "3":
            search_reservation_by_id_view(reservation_dao)
        elif option == "4":
            update_reservation_view(reservation_dao)
        elif option == "5":
            delete_reservation_view(reservation_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()