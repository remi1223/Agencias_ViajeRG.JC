class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password_hash: str,
        role: str = "user",
        user_id: int | None = None,
    ):
        if not first_name or not first_name.strip():
            raise ValueError("El nombre no puede quedar vacío.")
        if not last_name or not last_name.strip():
            raise ValueError("El apellido no puede quedar vacío.")
        if not email or "@" not in email:
            raise ValueError("Debe ingresar un correo electrónico válido.")
        if not password_hash or not password_hash.strip():
            raise ValueError("La contraseña encriptada no puede quedar vacía.")
        if role not in ("admin", "user"):
            raise ValueError("El rol debe ser 'admin' o 'user'.")

        self._user_id = user_id
        self._first_name = first_name.strip()
        self._last_name = last_name.strip()
        self._email = email.strip().lower()
        self._password_hash = password_hash.strip()
        self._role = role.strip().lower()

    def show_data(self) -> str:
        return (
            f"{self._user_id}-{self._first_name} {self._last_name}-"
            f"{self._email}-Rol: {self._role}"
        )
    