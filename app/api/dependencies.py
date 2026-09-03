from fastapi import Request


def db_path(request: Request) -> str:
    return request.app.state.db_path
