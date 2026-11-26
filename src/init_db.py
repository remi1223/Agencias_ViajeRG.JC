import hashlib
from persistencia.connection import abrir_conexion, marcador_sql


def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()


def initialize_database() -> None:
    placeholder = marcador_sql()
    is_sqlite = placeholder == "?"

    conn = None
    cursor = None
    try:
        conn = abrir_conexion()
        cursor = conn.cursor()

        if is_sqlite:
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(80) NOT NULL,
                    last_name VARCHAR(80) NOT NULL,
                    email VARCHAR(150) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS packages (
                    package_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(150) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    total_price NUMERIC(12, 2) NOT NULL,
                    available_slots INTEGER NOT NULL,
                    status BOOLEAN NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    package_id INTEGER NOT NULL,
                    reservation_date DATE NOT NULL,
                    number_of_people INTEGER NOT NULL,
                    total_amount NUMERIC(12, 2) NOT NULL,
                    status BOOLEAN NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (package_id) REFERENCES packages(package_id)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS destinations (
                    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(120) NOT NULL,
                    country_id INTEGER NOT NULL,
                    description VARCHAR(1000) NULL,
                    base_cost NUMERIC(12, 2) NOT NULL,
                    status BOOLEAN NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS package_destinations (
                    package_id INTEGER NOT NULL,
                    destination_id INTEGER NOT NULL,
                    PRIMARY KEY (package_id, destination_id),
                    FOREIGN KEY (package_id) REFERENCES packages(package_id) ON DELETE CASCADE,
                    FOREIGN KEY (destination_id) REFERENCES destinations(destination_id) ON DELETE CASCADE
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trip_status (
                    trip_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    description VARCHAR(50) NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transport_type (
                    transport_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    description VARCHAR(50) NULL
                );
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(80) NOT NULL,
                    last_name VARCHAR(80) NOT NULL,
                    email VARCHAR(150) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS packages (
                    package_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(150) NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    total_price DECIMAL(12, 2) NOT NULL,
                    available_slots INT NOT NULL,
                    status BOOLEAN NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    package_id INT NOT NULL,
                    reservation_date DATE NOT NULL,
                    number_of_people INT NOT NULL,
                    total_amount DECIMAL(12, 2) NOT NULL,
                    status BOOLEAN NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (package_id) REFERENCES packages(package_id)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS destinations (
                    destination_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(120) NOT NULL,
                    country_id INT NOT NULL,
                    description VARCHAR(1000) NULL,
                    base_cost DECIMAL(12, 2) NOT NULL,
                    status BOOLEAN NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS package_destinations (
                    package_id INT NOT NULL,
                    destination_id INT NOT NULL,
                    PRIMARY KEY (package_id, destination_id),
                    FOREIGN KEY (package_id) REFERENCES packages(package_id) ON DELETE CASCADE,
                    FOREIGN KEY (destination_id) REFERENCES destinations(destination_id) ON DELETE CASCADE
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trip_status (
                    trip_status_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    description VARCHAR(50) NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transport_type (
                    transport_type_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    description VARCHAR(50) NULL
                );
            """)

        default_users = [
            ("Admin", "Principal", "admin@viajes.cl", hash_password("admin123"), "admin"),
            ("Cliente", "Prueba", "user@viajes.cl", hash_password("user123"), "user"),
        ]

        for first_name, last_name, email, pwd_hash, role in default_users:
            cursor.execute(f"SELECT user_id FROM users WHERE email = {placeholder}", (email,))
            if not cursor.fetchone():
                cursor.execute(
                    f"""
                    INSERT INTO users (first_name, last_name, email, password_hash, role)
                    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
                    """,
                    (first_name, last_name, email, pwd_hash, role),
                )

        # Destinos iniciales de ejemplo para probar package_destinations de inmediato
        default_destinations = [
            ("San Pedro de Atacama", 1, "Desierto de Atacama y Valle de la Luna", 180000.0, True),
            ("Torres del Paine", 1, "Circuito trekking y glaciares en la Patagonia", 320000.0, True),
        ]

        for name, country_id, description, base_cost, status in default_destinations:
            cursor.execute(f"SELECT destination_id FROM destinations WHERE name = {placeholder}", (name,))
            if not cursor.fetchone():
                cursor.execute(
                    f"""
                    INSERT INTO destinations (name, country_id, description, base_cost, status)
                    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
                    """,
                    (name, country_id, description, base_cost, status),
                )

        conn.commit()
        print("Base de datos y credenciales inicializadas correctamente.")
        print("-> Admin: admin@viajes.cl / admin123")
        print("-> User:  user@viajes.cl  / user123")

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