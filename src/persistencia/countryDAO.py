import sqlite3
import pymysql
from persistencia.connection import abrir_conexion, marcador_sql
from dominio.country import Country


class CountryDAO:
    def __init__(self):
        self.placeholder = marcador_sql()

    def create_country(self, country: Country) -> int | None:
        query = f"INSERT INTO countries (name) VALUES ({self.placeholder})"
        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (country._name,))
            conn.commit()
            return cursor.lastrowid
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError):
            if conn:
                conn.rollback()
            raise ValueError("Ya existe un país registrado con ese nombre.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al crear país: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_countries(self) -> list[Country]:
        query = "SELECT country_id, name FROM countries ORDER BY country_id"
        conn = None
        cursor = None
        countries = []
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                countries.append(Country(country_id=row[0], name=row[1]))
            return countries
        except Exception as e:
            raise RuntimeError(f"Error al listar países: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_country_by_id(self, country_id: int) -> Country | None:
        query = f"SELECT country_id, name FROM countries WHERE country_id = {self.placeholder}"
        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (country_id,))
            row = cursor.fetchone()
            if row:
                return Country(country_id=row[0], name=row[1])
            return None
        except Exception as e:
            raise RuntimeError(f"Error al buscar país por ID: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_country(self, country: Country) -> bool:
        if not country._country_id:
            raise ValueError("El país debe tener un ID válido para actualizarse.")

        query = f"UPDATE countries SET name = {self.placeholder} WHERE country_id = {self.placeholder}"
        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (country._name, country._country_id))
            conn.commit()
            return cursor.rowcount > 0
        except (sqlite3.IntegrityError, pymysql.err.IntegrityError):
            if conn:
                conn.rollback()
            raise ValueError("Ya existe otro país con ese nombre.")
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al actualizar país: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_country(self, country_id: int) -> bool:
        query = f"DELETE FROM countries WHERE country_id = {self.placeholder}"
        conn = None
        cursor = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute(query, (country_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error al eliminar país (verifique que no tenga destinos asociados): {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()