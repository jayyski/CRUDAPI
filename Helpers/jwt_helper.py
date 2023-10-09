import jwt

SECRET_KEY = "secret"


def generate_admin_token() -> str:
    payload = {"username": "admin"}
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print(jwt_token)
    return jwt_token


def if_user_admin(jwt_token: str) -> bool:
    token = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
    if token["username"] == "admin":
        return True
