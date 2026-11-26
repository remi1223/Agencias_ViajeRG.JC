import sqlite3
import pymysql
from persistencia.connection import abrir_conexion, marcador_sql
from dominio.reservation import Reservation


class ReservationDAO:
    def __init__(self):
        self.placeholder = marcador_sql()

    def create_reservation(self, reservation: Reservation) -> int:
        query = f"""
            INSERT INTO reservations (user_id, package_id, reservation_date, number_of_people, total_amount, status)
            VALUES ({self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder})
        """
        params = (
            reservation._user_id,
            reservation._package_id,
            reservation._reservation_date,
            reservation._number_of_people,
            reservation._total_amount,
            reservation._status,
        )

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            reservation._reservation_id = cursor.lastrowid
            return reservation._reservation_id
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError):
            if conn:
                conn.rollback()
            raise ValueError("Error de integridad: Verifique que el ID de usuario y el ID de paquete existan.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al crear la reserva en la base de datos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservation_by_id(self, reservation_id: int) -> Reservation | None:
        query = f"""
            SELECT reservation_id, user_id, package_id, reservation_date, number_of_people, total_amount, status
            FROM reservations
            WHERE reservation_id = {self.placeholder}
        """

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (reservation_id,))
            row = cursor.fetchone()

            if row:
                return Reservation(
                    reservation_id=row[0],
                    user_id=row[1],
                    package_id=row[2],
                    reservation_date=row[3],
                    number_of_people=row[4],
                    total_amount=row[5],
                    status=bool(row[6]),
                )
            return None
        except Exception as e:
            raise RuntimeError(f"Error al obtener la reserva por ID: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservations_by_user(self, user_id: int) -> list[Reservation]:
        query = f"""
            SELECT reservation_id, user_id, package_id, reservation_date, number_of_people, total_amount, status
            FROM reservations
            WHERE user_id = {self.placeholder}
        """

        conn = None
        cursor = None
        reservations = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            for row in rows:
                reservations.append(
                    Reservation(
                        reservation_id=row[0],
                        user_id=row[1],
                        package_id=row[2],
                        reservation_date=row[3],
                        number_of_people=row[4],
                        total_amount=row[5],
                        status=bool(row[6]),
                    )
                )
            return reservations
        except Exception as e:
            raise RuntimeError(f"Error al buscar las reservas del usuario: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_reservations(self) -> list[Reservation]:
        query = """
            SELECT reservation_id, user_id, package_id, reservation_date, number_of_people, total_amount, status
            FROM reservations
        """

        conn = None
        cursor = None
        reservations = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                reservations.append(
                    Reservation(
                        reservation_id=row[0],
                        user_id=row[1],
                        package_id=row[2],
                        reservation_date=row[3],
                        number_of_people=row[4],
                        total_amount=row[5],
                        status=bool(row[6]),
                    )
                )
            return reservations
        except Exception as e:
            raise RuntimeError(f"Error al listar las reservas: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_reservation(self, reservation: Reservation) -> bool:
        if reservation._reservation_id is None:
            raise ValueError("No se puede actualizar una reserva sin un ID válido.")

        query = f"""
            UPDATE reservations
            SET user_id = {self.placeholder},
                package_id = {self.placeholder},
                reservation_date = {self.placeholder},
                number_of_people = {self.placeholder},
                total_amount = {self.placeholder},
                status = {self.placeholder}
            WHERE reservation_id = {self.placeholder}
        """
        params = (
            reservation._user_id,
            reservation._package_id,
            reservation._reservation_date,
            reservation._number_of_people,
            reservation._total_amount,
            reservation._status,
            reservation._reservation_id,
        )

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError):
            if conn:
                conn.rollback()
            raise ValueError("Error de integridad: Verifique que el ID de usuario y el ID de paquete existan.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al actualizar la reserva: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_reservation(self, reservation_id: int) -> bool:
        query = f"DELETE FROM reservations WHERE reservation_id = {self.placeholder}"

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (reservation_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al eliminar la reserva: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()