import sqlite3
import pymysql
from persistencia.connection import abrir_conexion, marcador_sql  
from dominio.user import User


class UserDAO:
    def __init__(self):
        self.placeholder = marcador_sql()  

    def create_user(self, user: User) -> int:
        query = f"""
            INSERT INTO users (first_name, last_name, email, password_hash, role)
            VALUES ({self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder})
        """  #[cite: 1]
        params = (
            user._first_name,
            user._last_name,
            user._email,
            user._password_hash,
            user._role,
        )

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()  #[cite: 1]
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            user._user_id = cursor.lastrowid
            return user._user_id
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError):
            if conn:
                conn.rollback()
            raise ValueError("El correo electrónico ya se encuentra registrado.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al crear el usuario en la base de datos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_user_by_id(self, user_id: int) -> User | None:
        query = f"""
            SELECT user_id, first_name, last_name, email, password_hash, role
            FROM users
            WHERE user_id = {self.placeholder}
        """  #[cite: 1]

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()  #[cite: 1]
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()

            if row:
                return User(
                    user_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    pasword_hash=row[4],
                    role=row[5],
                )
            return None
        except Exception as e:
            raise RuntimeError(f"Error al obtener el usuario por ID: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_user_by_email(self, email: str) -> User | None:
        query = f"""
            SELECT user_id, first_name, last_name, email, password_hash, role
            FROM users
            WHERE email = {self.placeholder}
        """  #[cite: 1]

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()  #[cite: 1]
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            row = cursor.fetchone()

            if row:
                return User(
                    user_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    pasword_hash=row[4],
                    role=row[5],
                )
            return None
        except Exception as e:
            raise RuntimeError(f"Error al buscar el usuario por correo: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_users(self) -> list[User]:
        query = """
            SELECT user_id, first_name, last_name, email, password_hash, role
            FROM users
        """

        conn = None
        cursor = None
        users = []
        try:
            conn = abrir_conexion()  #[cite: 1]
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                users.append(
                    User(
                        user_id=row[0],
                        first_name=row[1],
                        last_name=row[2],
                        email=row[3],
                        pasword_hash=row[4],
                        role=row[5],
                    )
                )
            return users
        except Exception as e:
            raise RuntimeError(f"Error al listar los usuarios: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_user(self, user: User) -> bool:
        if user._user_id is None:
            raise ValueError("No se puede actualizar un usuario sin un ID válido.")

        query = f"""
            UPDATE users
            SET first_name = {self.placeholder},
                last_name = {self.placeholder},
                email = {self.placeholder},
                password_hash = {self.placeholder},
                role = {self.placeholder}
            WHERE user_id = {self.placeholder}
        """  #[cite: 1]
        params = (
            user._first_name,
            user._last_name,
            user._email,
            user._password_hash,
            user._role,
            user._user_id,
        )

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()  #[cite: 1]
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError):
            if conn:
                conn.rollback()
            raise ValueError("El correo electrónico ya está en uso por otro usuario.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al actualizar el usuario: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_user(self, user_id: int) -> bool:
        query = f"DELETE FROM users WHERE user_id = {self.placeholder}"  #[cite: 1]

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()  #[cite: 1]
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al eliminar el usuario: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()