import sqlite3

import jwt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from Database import queries
from Models import models
from Helpers import jwt_helper

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/users/", response_model=list[dict[str, str]])
async def read_items(token: str = Depends(oauth2_scheme)) -> list[dict[str, str]]:
    try:
        if not jwt_helper.if_user_admin(token):
            raise HTTPException(status_code=401, detail="Unauthorized")

        users = queries.get_all_users()

        if users is None:
            raise HTTPException(status_code=404, detail="Users not found")

        users_list = []
        for user in users:
            user_dict = dict(username=user[0], password=user[1])
            users_list.append(user_dict)

        return users_list
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=404, detail="Could not decode token")


@app.post("/create_user/", response_model=models.User)
async def create_user(user: models.User) -> dict[str, str]:
    if user.username == "admin" or user.password == "adminadmin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        queries.create_user(user.username, user.password)
        return {"username": user.username, "password": user.password}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Unique username required")


@app.get("/user/{username}", response_model=models.User)
async def get_user(username: str) -> dict[str, str]:
    user = queries.get_by_username(username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = dict(username=user[0], password=user[1])
    return user_dict


@app.delete("/user/{username}", response_model=dict[str, str])
async def delete_user(username: str, token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    try:
        if not jwt_helper.if_user_admin(token):
            raise HTTPException(status_code=401, detail="Unauthorized")

        if not queries.if_user_exists(username):
            raise HTTPException(status_code=404, detail="User not found")

        return queries.delete_by_username(username)

    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=404, detail="Could not decode token")


@app.post("/token", response_model=dict[str, str])
async def get_token(user: models.User) -> dict[str, str]:
    if user.username != "admin" and user.password != "adminadmin":
        raise HTTPException(status_code=401, detail="Incorrect username and password")
    return {"token": jwt_helper.generate_admin_token()}