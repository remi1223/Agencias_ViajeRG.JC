import sqlite3
import pymysql
from persistencia.connection import abrir_conexion, marcador_sql
from dominio.package_destinations import PackageDestination
from dominio.destination import Destination


class PackageDestinationsDAO:
    def __init__(self):
        self.placeholder = marcador_sql()

    def add_destination_to_package(self, relation: PackageDestination) -> bool:
        query = f"""
            INSERT INTO package_destinations (package_id, destination_id)
            VALUES ({self.placeholder}, {self.placeholder})
        """
        params = (relation._package_id, relation._destination_id)

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
            raise ValueError(
                "No se pudo asignar: el destino ya está asociado a este paquete, "
                "o el ID de paquete/destino no existe."
            )
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al asignar destino al paquete: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_package_destinations_detailed(self) -> list[dict]:
        query = """
            SELECT pd.package_id, p.name, pd.destination_id, d.name
            FROM package_destinations pd
            INNER JOIN packages p ON pd.package_id = p.package_id
            INNER JOIN destinations d ON pd.destination_id = d.destination_id
            ORDER BY pd.package_id, d.name
        """

        conn = None
        cursor = None
        results = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                results.append({
                    "package_id": row[0],
                    "package_name": row[1],
                    "destination_id": row[2],
                    "destination_name": row[3],
                })
            return results
        except Exception as e:
            raise RuntimeError(f"Error al listar asignaciones de destinos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_destination_details_by_package(self, package_id: int) -> list[Destination]:
        query = f"""
            SELECT d.destination_id, d.name, d.country_id, d.description, d.base_cost, d.status
            FROM destinations d
            INNER JOIN package_destinations pd ON d.destination_id = pd.destination_id
            WHERE pd.package_id = {self.placeholder}
              AND d.status = 1
            ORDER BY d.name
        """

        conn = None
        cursor = None
        destinations = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (package_id,))
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
            raise RuntimeError(f"Error al obtener los detalles de destinos del paquete: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def remove_destination_from_package(self, package_id: int, destination_id: int) -> bool:
        query = f"""
            DELETE FROM package_destinations
            WHERE package_id = {self.placeholder}
              AND destination_id = {self.placeholder}
        """

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (package_id, destination_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al quitar destino del paquete: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()