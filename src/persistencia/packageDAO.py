import sqlite3
import pymysql
from persistencia.connection import abrir_conexion, marcador_sql
from dominio.package import Package

class PackageDAO:
    def __init__(self):
        self.placeholder = marcador_sql()

    def create_package(self, package: Package) -> int:
        query = f"""
            INSERT INTO packages (name, start_date, end_date, total_price, available_slots, status)
            VALUES ({self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder}, {self.placeholder})
        """
        params = (
            package._name,
            package._start_date,
            package._end_date,
            package._total_price,
            package._available_slots,
            package._status,
        )

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            package._package_id = cursor.lastrowid
            return package._package_id
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError) as e:
            if conn:
                conn.rollback()
            raise ValueError(f"Error de integridad al crear el paquete: {e}")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al crear el paquete en la base de datos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_package_by_id(self, package_id: int) -> Package | None:
        query = f"""
            SELECT package_id, name, start_date, end_date, total_price, available_slots, status
            FROM packages
            WHERE package_id = {self.placeholder}
        """

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (package_id,))
            row = cursor.fetchone()

            if row:
                return Package(
                    package_id=row[0],
                    name=row[1],
                    start_date=row[2],
                    end_date=row[3],
                    total_price=row[4],
                    available_slots=row[5],
                    status=bool(row[6]),
                )
            return None
        except Exception as e:
            raise RuntimeError(f"Error al obtener el paquete por ID: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_packages(self) -> list[Package]:
        query = """
            SELECT package_id, name, start_date, end_date, total_price, available_slots, status
            FROM packages
        """

        conn = None
        cursor = None
        packages = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                packages.append(
                    Package(
                        package_id=row[0],
                        name=row[1],
                        start_date=row[2],
                        end_date=row[3],
                        total_price=row[4],
                        available_slots=row[5],
                        status=bool(row[6]),
                    )
                )
            return packages
        except Exception as e:
            raise RuntimeError(f"Error al listar los paquetes: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_available_packages(self) -> list[Package]:
        query = f"""
            SELECT package_id, name, start_date, end_date, total_price, available_slots, status
            FROM packages
            WHERE status = {self.placeholder} AND available_slots > 0
        """

        conn = None
        cursor = None
        packages = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (True,))
            rows = cursor.fetchall()

            for row in rows:
                packages.append(
                    Package(
                        package_id=row[0],
                        name=row[1],
                        start_date=row[2],
                        end_date=row[3],
                        total_price=row[4],
                        available_slots=row[5],
                        status=bool(row[6]),
                    )
                )
            return packages
        except Exception as e:
            raise RuntimeError(f"Error al listar los paquetes disponibles: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_package(self, package: Package) -> bool:
        if package._package_id is None:
            raise ValueError("No se puede actualizar un paquete sin un ID válido.")

        query = f"""
            UPDATE packages
            SET name = {self.placeholder},
                start_date = {self.placeholder},
                end_date = {self.placeholder},
                total_price = {self.placeholder},
                available_slots = {self.placeholder},
                status = {self.placeholder}
            WHERE package_id = {self.placeholder}
        """
        params = (
            package._name,
            package._start_date,
            package._end_date,
            package._total_price,
            package._available_slots,
            package._status,
            package._package_id,
        )

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al actualizar el paquete: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_package(self, package_id: int) -> bool:
        query = f"DELETE FROM packages WHERE package_id = {self.placeholder}"

        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (package_id,))
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError):
            if conn:
                conn.rollback()
            raise ValueError("No se puede eliminar el paquete porque tiene reservas asociadas.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al eliminar el paquete: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()