from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request


def register_validation(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception(request: Request, exc: RequestValidationError):
        errors = []

        for err in exc.errors():
            errors.append({
                "field": err["loc"][-1],
                "error": err["msg"]
            })

        return JSONResponse(
            status_code=400,
            content={"errors": errors}
        )