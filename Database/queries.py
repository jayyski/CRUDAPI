from typing import Any, Sequence
import sqlite3
import jwt

DATABASE = "/home/user/PycharmProjects/fastApiProject/test.db"


def get_all_users() -> Sequence[Any]:
    with sqlite3.connect(DATABASE) as con:
        user_rows = con.execute("SELECT username, password FROM users").fetchall()
        return user_rows


def create_user(username: str, password: str) -> None:
    with sqlite3.connect(DATABASE) as con:
        con.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
        return None


def get_by_username(username: str) -> Sequence[Any]:
    with sqlite3.connect(DATABASE) as con:
        user_row = con.execute("SELECT username, password FROM users WHERE username = ?", (username,)).fetchone()
        return user_row


def delete_by_username(username: str) -> dict[str, str]:
    with sqlite3.connect(DATABASE) as con:
        con.execute("DELETE FROM users WHERE username = ?", (username,))
        con.commit()
        return {"deleted successfully": username}


def if_user_exists(username: str) -> bool:
    with sqlite3.connect(DATABASE) as con:
        user_row = con.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()
        if user_row is None:
            return False
        return True