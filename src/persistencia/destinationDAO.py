import sqlite3
import pymysql
from persistencia.connection import abrir_conexion, marcador_sql
from dominio.destination import Destination


class DestinationDAO:
    def __init__(self):
        self.placeholder = marcador_sql()

    def create_destination(self, destination: Destination) -> int | None:
        query = f"""
            INSERT INTO destinations (name, country_id, description, base_cost, status)
            VALUES ({self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder})
        """
        params = (
            destination._name,
            destination._country_id,
            destination._description,
            destination._base_cost,
            destination._status,
        )

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError):
            if conn:
                conn.rollback()
            raise ValueError("No se pudo crear el destino: verifique el ID del país o restricciones de datos.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al crear destino: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_destinations(self) -> list[Destination]:
        query = """
            SELECT destination_id, name, country_id, description, base_cost, status
            FROM destinations
            ORDER BY destination_id
        """

        conn = None
        cursor = None
        destinations = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                destinations.append(
                    Destination(
                        destination_id=row[0],
                        name=row[1],
                        country_id=row[2],
                        description=row[3],
                        base_cost=float(row[4]),
                        status=bool(row[5]),
                    )
                )
            return destinations
        except Exception as e:
            raise RuntimeError(f"Error al listar destinos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_destination_by_id(self, destination_id: int) -> Destination | None:
        query = f"""
            SELECT destination_id, name, country_id, description, base_cost, status
            FROM destinations
            WHERE destination_id = {self.placeholder}
        """

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (destination_id,))
            row = cursor.fetchone()

            if row:
                return Destination(
                    destination_id=row[0],
                    name=row[1],
                    country_id=row[2],
                    description=row[3],
                    base_cost=float(row[4]),
                    status=bool(row[5]),
                )
            return None
        except Exception as e:
            raise RuntimeError(f"Error al buscar destino por ID: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_destination(self, destination: Destination) -> bool:
        if not destination._destination_id:
            raise ValueError("El destino debe tener un ID válido para actualizarse.")

        query = f"""
            UPDATE destinations
            SET name = {self.placeholder},
                country_id = {self.placeholder},
                description = {self.placeholder},
                base_cost = {self.placeholder},
                status = {self.placeholder}
            WHERE destination_id = {self.placeholder}
        """
        params = (
            destination._name,
            destination._country_id,
            destination._description,
            destination._base_cost,
            destination._status,
            destination._destination_id,
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
            raise ValueError("No se pudo actualizar: verifique los datos ingresados.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al actualizar destino: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_destination(self, destination_id: int) -> bool:
        query = f"DELETE FROM destinations WHERE destination_id = {self.placeholder}"

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (destination_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al eliminar destino: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()