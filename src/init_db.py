import hashlib
import os
from persistencia.connection import abrir_conexion


def _hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()


def initialize_database() -> None:
    db_engine = os.getenv("DB_ENGINE", "sqlite").strip().lower()
    is_mysql = db_engine == "mysql"

    pk_auto = "INT AUTO_INCREMENT PRIMARY KEY" if is_mysql else "INTEGER PRIMARY KEY AUTOINCREMENT"
    insert_ignore = "INSERT IGNORE INTO" if is_mysql else "INSERT OR IGNORE INTO"
    placeholder = "%s" if is_mysql else "?"

    tables_sql = [
        f"""
        CREATE TABLE IF NOT EXISTS users (
            user_id {pk_auto},
            first_name VARCHAR(80) NOT NULL,
            last_name VARCHAR(80) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS countries (
            country_id {pk_auto},
            name VARCHAR(100) NOT NULL UNIQUE
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS destinations (
            destination_id {pk_auto},
            name VARCHAR(120) NOT NULL,
            country_id INT NOT NULL,
            description VARCHAR(1000) NULL,
            base_cost DECIMAL(12, 2) NOT NULL,
            status BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (country_id) REFERENCES countries(country_id)
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS packages (
            package_id {pk_auto},
            name VARCHAR(150) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            total_price DECIMAL(12, 2) NOT NULL,
            available_slots INT NOT NULL,
            status BOOLEAN NOT NULL DEFAULT 1
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS package_destinations (
            package_id INT NOT NULL,
            destination_id INT NOT NULL,
            PRIMARY KEY (package_id, destination_id),
            FOREIGN KEY (package_id) REFERENCES packages(package_id) ON DELETE CASCADE,
            FOREIGN KEY (destination_id) REFERENCES destinations(destination_id) ON DELETE CASCADE
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id {pk_auto},
            user_id INT NOT NULL,
            package_id INT NOT NULL,
            reservation_date DATE NOT NULL,
            number_of_people INT NOT NULL,
            total_amount DECIMAL(12, 2) NOT NULL,
            status BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (package_id) REFERENCES packages(package_id)
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS trip_status (
            trip_status_id {pk_auto},
            name VARCHAR(50) NOT NULL UNIQUE,
            description VARCHAR(255) NULL
        );
        """,
        f"""
        CREATE TABLE IF NOT EXISTS transport_type (
            transport_type_id {pk_auto},
            name VARCHAR(50) NOT NULL UNIQUE,
            description VARCHAR(255) NULL
        );
        """,
    ]

    conn = None
    cursor = None
    try:
        conn = abrir_conexion()
        cursor = conn.cursor()

        if not is_mysql:
            cursor.execute("PRAGMA foreign_keys = ON;")

        for ddl in tables_sql:
            cursor.execute(ddl)

        # 1. Usuarios iniciales (Admin y Cliente)
        initial_users = [
            (1, "Admin", "Sistema", "admin@viajes.cl", _hash_password("admin123"), "admin"),
            (2, "Cliente", "Aventura", "user@viajes.cl", _hash_password("user123"), "user"),
        ]
        cursor.executemany(
            f"""
            {insert_ignore} users (user_id, first_name, last_name, email, password_hash, role)
            VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """,
            initial_users,
        )

        # 2. Países iniciales (para paquetes nacionales e internacionales)
        initial_countries = [
            (1, "Chile"),
            (2, "Perú"),
            (3, "Brasil"),
            (4, "Argentina"),
            (5, "España"),
        ]
        cursor.executemany(
            f"""
            {insert_ignore} countries (country_id, name)
            VALUES ({placeholder}, {placeholder})
            """,
            initial_countries,
        )

        # 3. Destinos iniciales vinculados a sus países
        initial_destinations = [
            (1, "San Pedro de Atacama", 1, "Desierto, géiseres del Tatio y Valle de la Luna", 180000.0, True),
            (2, "Torres del Paine", 1, "Trekking en la Patagonia chilena y glaciares", 250000.0, True),
            (3, "Cusco y Machu Picchu", 2, "Ciudadela inca y Valle Sagrado", 320000.0, True),
            (4, "Río de Janeiro", 3, "Playas de Copacabana y Cristo Redentor", 290000.0, True),
            (5, "Buenos Aires", 4, "Ruta gastronómica, tango y recorrido histórico", 210000.0, True),
        ]
        cursor.executemany(
            f"""
            {insert_ignore} destinations (destination_id, name, country_id, description, base_cost, status)
            VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """,
            initial_destinations,
        )

        # 4. Estados de viaje iniciales
        initial_trip_statuses = [
            (1, "Programado", "Viaje confirmado y próximo a iniciar"),
            (2, "En curso", "El viaje se encuentra actualmente en desarrollo"),
            (3, "Finalizado", "Itinerario completado sin novedades"),
            (4, "Cancelado", "Viaje suspendido"),
        ]
        cursor.executemany(
            f"""
            {insert_ignore} trip_status (trip_status_id, name, description)
            VALUES ({placeholder}, {placeholder}, {placeholder})
            """,
            initial_trip_statuses,
        )

        # 5. Tipos de transporte iniciales
        initial_transports = [
            (1, "Avión", "Vuelo comercial nacional o internacional"),
            (2, "Bus Ejecutivo", "Transporte terrestre interurbano"),
            (3, "Transfer Privado", "Traslado aeropuerto - hotel - excursiones"),
            (4, "Crucero / Catamarán", "Navegación marítima o lacustre"),
        ]
        cursor.executemany(
            f"""
            {insert_ignore} transport_type (transport_type_id, name, description)
            VALUES ({placeholder}, {placeholder}, {placeholder})
            """,
            initial_transports,
        )

        conn.commit()
        print("Base de datos verificada e inicializada correctamente.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    initialize_database()