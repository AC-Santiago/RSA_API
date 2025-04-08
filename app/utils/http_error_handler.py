from fastapi import FastAPI, status
from fastapi.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request


class HTTPErrorHandler(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            contente = f"{str(e)}"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(content={"detail": contente}, status_code=status_code)
