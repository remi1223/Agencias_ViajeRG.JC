import hashlib
from dominio.user import User
from persistencia.userDAO import UserDAO
from presentation.menu_user import run_user_menu
from presentation.menu_package import run_package_menu
from presentation.menu_reservation import run_reservation_menu, run_client_reservation_menu
from presentation.menu_destination import run_destination_menu
from presentation.menu_package_destination import run_package_destinations_menu
from init_db import initialize_database
from complementos.plugins import clean_screen, pause_and_clean


def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()


def login_view(user_dao: UserDAO) -> User | None:
    clean_screen()
    print("===============================")
    print("       INICIAR SESIÓN")
    print("===============================")
    email = input("Correo electrónico: ").strip().lower()
    raw_password = input("Contraseña: ").strip()

    if not email or not raw_password:
        print("\nError: Debe ingresar correo y contraseña.")
        pause_and_clean()
        return None

    try:
        user = user_dao.get_user_by_email(email)
        if not user:
            print("\nCredenciales incorrectas.")
            pause_and_clean()
            return None

        if user._password_hash != hash_password(raw_password):
            print("\nCredenciales incorrectas.")
            pause_and_clean()
            return None

        print(f"\n¡Bienvenido/a, {user._first_name} ({user._role})!")
        pause_and_clean()
        return user

    except RuntimeError as e:
        print(f"\nError del sistema: {e}")
        pause_and_clean()
        return None


def authenticated_menu(current_user: User) -> None:
    while True:
        clean_screen()
        print("===============================")
        print("   SISTEMA AGENCIA DE VIAJES")
        print(f"   Usuario: {current_user._first_name} | Rol: {current_user._role}")
        print("===============================")

        if current_user._role == "admin":
            print("1. Gestionar usuarios")
            print("2. Gestionar paquetes")
            print("3. Gestionar reservas")
            print("4. Gestionar destinos")
            print("5. Gestionar destinos por paquete")
            print("0. Cerrar sesión")

            option = input("Seleccione una opción: ").strip()

            if option == "1":
                run_user_menu()
            elif option == "2":
                run_package_menu()
            elif option == "3":
                run_reservation_menu()
            elif option == "4":
                run_destination_menu()
            elif option == "5":
                run_package_destinations_menu()
            elif option == "0":
                clean_screen()
                print("Sesión cerrada.")
                pause_and_clean()
                break
            else:
                print("\nOpción no válida. Intente nuevamente.")
                pause_and_clean()
        else:
            print("1. Contratar o ver mis paquetes")
            print("0. Cerrar sesión")

            option = input("Seleccione una opción: ").strip()

            if option == "1":
                run_client_reservation_menu(current_user)
            elif option == "0":
                clean_screen()
                print("Sesión cerrada.")
                pause_and_clean()
                break
            else:
                print("\nOpción no válida. Intente nuevamente.")
                pause_and_clean()


def main_menu() -> None:
    initialize_database()
    pause_and_clean()
    user_dao = UserDAO()

    while True:
        clean_screen()
        print("===============================")
        print("   AGENCIA DE VIAJES RG.JC")
        print("===============================")
        print("1. Iniciar sesión")
        print("0. Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            logged_user = login_view(user_dao)
            if logged_user:
                authenticated_menu(logged_user)
        elif option == "0":
            clean_screen()
            print("Hasta pronto.")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()


if __name__ == "__main__":
    main_menu()