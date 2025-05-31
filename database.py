import sqlite3
import hashlib
import os
from sqlite3 import Error

DB_PATH = os.path.join(os.path.dirname(__file__), 'pluschka.db')


def create_connection():
    """Создает и возвращает соединение с базой данных"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Error as e:
        print(f"Ошибка подключения: {e}")
        return None


def hash_password(password: str) -> str:
    """Хеширует пароль с SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def init_db(force=False):
    """
    Инициализирует таблицы в базе данных
    :param force: явно пересоздать все таблицы
    """
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        if force:

            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("DROP TABLE IF EXISTS event_attendance")

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS users
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           name
                           TEXT
                           NOT
                           NULL,
                           email
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           role
                           TEXT
                           NOT
                           NULL
                           DEFAULT
                           'student',
                           password_hash
                           TEXT
                           NOT
                           NULL,
                           about
                           TEXT
                           DEFAULT
                           '',
                           photo
                           BLOB
                           DEFAULT
                           NULL,
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP
                       )""")

        # Создаем таблицу записи на мероприятия
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS event_attendance
                       (
                           user_id
                           INTEGER
                           NOT
                           NULL,
                           event_id
                           INTEGER
                           NOT
                           NULL
                           DEFAULT
                           1,
                           FOREIGN
                           KEY
                       (
                           user_id
                       ) REFERENCES users
                       (
                           id
                       ) ON DELETE CASCADE,
                           PRIMARY KEY
                       (
                           user_id,
                           event_id
                       )
                           )""")

        conn.commit()
        print("Таблицы успешно инициализированы")
        return True
    except Error as e:
        print(f"Ошибка инициализации БД: {e}")
        return False
    finally:
        if conn:
            conn.close()


def check_db_exists():
    """Проверяет, инициализирована ли БД"""
    if not os.path.exists(DB_PATH):
        return False

    required_tables = {'users', 'event_attendance'}
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = {row[0] for row in cursor.fetchall()}
        return required_tables.issubset(existing_tables)
    finally:
        if conn:
            conn.close()


def register_user(name: str, email: str, password: str, role: str = "student") -> int:
    """Регистрирует нового пользователя и возвращает его ID"""
    conn = create_connection()
    if not conn:
        return -1

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, role, password_hash) VALUES (?, ?, ?, ?)",
            (name, email, role, hash_password(password))
        )
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        print(f"Ошибка: email {email} уже существует")
        return -1
    except Error as e:
        print(f"Ошибка регистрации: {e}")
        return -1
    finally:
        if conn:
            conn.close()


def check_credentials(email: str, password: str) -> int:
    """Проверяет email и пароль, возвращает ID пользователя или -1"""
    conn = create_connection()
    if not conn:
        return -1

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE email = ?",
            (email,))
        row = cursor.fetchone()
        if row and row[1] == hash_password(password):
            return row[0]  # Возвращаем ID пользователя
        return -1
    except Error as e:
        print(f"Ошибка проверки: {e}")
        return -1
    finally:
        if conn:
            conn.close()


def update_profile(user_id: int, name: str, about: str, photo_path: str = None) -> bool:
    """Обновляет данные профиля пользователя"""
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        if photo_path:
            try:
                with open(photo_path, 'rb') as f:
                    photo_data = f.read()
                cursor.execute(
                    "UPDATE users SET name = ?, about = ?, photo = ? WHERE id = ?",
                    (name, about, photo_data, user_id))
            except Exception as e:
                print(f"Ошибка загрузки фото: {e}")
                cursor.execute(
                    "UPDATE users SET name = ?, about = ? WHERE id = ?",
                    (name, about, user_id))
        else:
            cursor.execute(
                "UPDATE users SET name = ?, about = ? WHERE id = ?",
                (name, about, user_id))

        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Ошибка обновления профиля: {e}")
        return False
    finally:
        if conn:
            conn.close()


def register_for_event(user_id: int, event_id: int = 1) -> bool:
    """Регистрирует пользователя на мероприятие"""
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO event_attendance (user_id, event_id) VALUES (?, ?)",
            (user_id, event_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Ошибка записи на мероприятие: {e}")
        return False
    finally:
        if conn:
            conn.close()


def is_registered_for_event(user_id: int, event_id: int = 1) -> bool:
    """Проверяет, записан ли пользователь на мероприятие"""
    conn = create_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM event_attendance WHERE user_id = ? AND event_id = ?",
            (user_id, event_id))
        return cursor.fetchone() is not None
    except Error as e:
        print(f"Ошибка проверки записи: {e}")
        return False
    finally:
        if conn:
            conn.close()


# Инициализация базы данных при первом запуске
if not check_db_exists():
    print("Инициализация новой базы данных...")
    init_db(force=True)