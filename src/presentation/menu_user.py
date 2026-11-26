import hashlib
from dominio.user import User
from persistencia.userDAO import UserDAO
from complementos.plugins import clean_screen, pause_and_clean


def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()


def read_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Error: Debe ingresar un número entero válido.")


def create_user_view(user_dao: UserDAO) -> None:
    clean_screen()
    print("--- REGISTRAR NUEVO USUARIO ---")
    try:
        first_name = input("Nombre: ").strip()
        last_name = input("Apellido: ").strip()
        email = input("Correo electrónico: ").strip()
        raw_password = input("Contraseña: ").strip()
        role = input("Rol (admin / user): ").strip().lower()

        if not raw_password:
            raise ValueError("La contraseña no puede quedar vacía.")

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hash_password(raw_password),
            role=role,
        )

        new_id = user_dao.create_user(new_user)
        print(f"\nUsuario registrado exitosamente con ID: {new_id}")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def list_users_view(user_dao: UserDAO) -> None:
    clean_screen()
    print("--- LISTA DE USUARIOS ---")
    try:
        users = user_dao.get_all_users()
        if not users:
            print("No hay usuarios registrados en el sistema.")
        else:
            for user in users:
                print(user.show_data())

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def search_user_view(user_dao: UserDAO) -> None:
    clean_screen()
    print("--- BUSCAR USUARIO ---")
    user_id = read_int("Ingrese el ID del usuario: ")

    try:
        user = user_dao.get_user_by_id(user_id)
        if user:
            print(f"\nUsuario encontrado: {user.show_data()}")
        else:
            print("\nNo se encontró ningún usuario con ese ID.")

    except RuntimeError as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def update_user_view(user_dao: UserDAO) -> None:
    clean_screen()
    print("--- ACTUALIZAR USUARIO ---")
    user_id = read_int("Ingrese el ID del usuario a modificar: ")

    try:
        existing = user_dao.get_user_by_id(user_id)
        if not existing:
            print("\nNo existe un usuario con ese ID.")
            return

        print(f"\nDatos actuales: {existing.show_data()}")
        print("(Presione Enter para mantener el valor actual)")

        first_str = input(f"Nuevo nombre [{existing._first_name}]: ").strip()
        last_str = input(f"Nuevo apellido [{existing._last_name}]: ").strip()
        email_str = input(f"Nuevo correo [{existing._email}]: ").strip()
        pass_str = input("Nueva contraseña (dejar vacío para mantener): ").strip()
        role_str = input(f"Nuevo rol (admin / user) [{existing._role}]: ").strip().lower()

        updated_first = first_str if first_str else existing._first_name
        updated_last = last_str if last_str else existing._last_name
        updated_email = email_str if email_str else existing._email
        updated_pass = hash_password(pass_str) if pass_str else existing._password_hash
        updated_role = role_str if role_str else existing._role

        updated_user = User(
            user_id=existing._user_id,
            first_name=updated_first,
            last_name=updated_last,
            email=updated_email,
            password_hash=updated_pass,
            role=updated_role,
        )

        if user_dao.update_user(updated_user):
            print("\nUsuario actualizado correctamente.")
        else:
            print("\nNo se realizaron cambios en el usuario.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def delete_user_view(user_dao: UserDAO) -> None:
    clean_screen()
    print("--- ELIMINAR USUARIO ---")
    user_id = read_int("Ingrese el ID del usuario a eliminar: ")

    try:
        user = user_dao.get_user_by_id(user_id)
        if not user:
            print("\nNo existe un usuario con ese ID.")
            return

        print(f"\nUsuario a eliminar: {user.show_data()}")
        confirm = input("¿Está seguro de eliminar este usuario? (s/n): ").strip().lower()

        if confirm == "s":
            if user_dao.delete_user(user_id):
                print("\nUsuario eliminado correctamente.")
            else:
                print("\nNo se pudo eliminar el usuario.")
        else:
            print("\nOperación cancelada.")

    except (ValueError, RuntimeError) as e:
        print(f"\nError: {e}")
    finally:
        pause_and_clean()


def run_user_menu() -> None:
    user_dao = UserDAO()

    while True:
        clean_screen()
        print("===============================")
        print("     GESTIÓN DE USUARIOS")
        print("===============================")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Buscar usuario por ID")
        print("4. Actualizar usuario")
        print("5. Eliminar usuario")
        print("0. Volver / Salir")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            create_user_view(user_dao)
        elif option == "2":
            list_users_view(user_dao)
        elif option == "3":
            search_user_view(user_dao)
        elif option == "4":
            update_user_view(user_dao)
        elif option == "5":
            delete_user_view(user_dao)
        elif option == "0":
            clean_screen()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            pause_and_clean()


if __name__ == "__main__":
    run_user_menu()