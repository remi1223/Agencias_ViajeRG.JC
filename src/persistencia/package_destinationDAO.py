import sqlite3
import pymysql
from persistencia.connection import abrir_conexion, marcador_sql
from dominio.package_destinations import PackageDestination


class PackageDestinationsDAO:
    def __init__(self):
        self.placeholder = marcador_sql()

    def add_destination_to_package(self, pkg_dest: PackageDestination) -> bool:
        query = f"""
            INSERT INTO package_destinations (package_id, destination_id)
            VALUES ({self.placeholder}, {self.placeholder})
        """
        params = (pkg_dest._package_id, pkg_dest._destination_id)

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
                "No se pudo asociar: este destino ya está asignado al paquete o uno de los IDs no existe."
            )
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al asociar destino al paquete: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_package_destinations(self) -> list[PackageDestination]:
        query = """
            SELECT package_id, destination_id
            FROM package_destinations
            ORDER BY package_id, destination_id
        """

        conn = None
        cursor = None
        relations = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                relations.append(
                    PackageDestination(
                        package_id=row[0],
                        destination_id=row[1],
                    )
                )
            return relations
        except Exception as e:
            raise RuntimeError(f"Error al listar las asociaciones paquete-destino: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_destinations_by_package(self, package_id: int) -> list[PackageDestination]:
        query = f"""
            SELECT package_id, destination_id
            FROM package_destinations
            WHERE package_id = {self.placeholder}
        """

        conn = None
        cursor = None
        relations = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (package_id,))
            rows = cursor.fetchall()

            for row in rows:
                relations.append(
                    PackageDestination(
                        package_id=row[0],
                        destination_id=row[1],
                    )
                )
            return relations
        except Exception as e:
            raise RuntimeError(f"Error al buscar destinos del paquete: {e}")
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
            raise RuntimeError(f"Error al eliminar destino del paquete: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()