from os import stat
from fastapi import Request
from fastapi.responses import JSONResponse

from src.services.exceptions import MetricsNotFoundError, ProductAlreadyExistsError, ProductNotFoundError, StoreAlreadyExistsError, StoreNotFoundError, UserAlreadyExistsError, UserNotFoundError


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError
):

    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"User with id {exc.user_id} doesn't exist"
        }
    )


async def user_atready_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError
):

    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"User with email {exc.email} already exists"
        }
    )


async def store_not_found_handler(
    request: Request,
    exc: StoreNotFoundError
):

    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Store with id {exc.store_id} doesn't exist"
        }
    )


async def store_already_exists_handler(
    request: Request,
    exc: StoreAlreadyExistsError
):

    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Store with name {exc.name} already exists"
            }
    )


async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundError
):

    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Product with id {exc.product_id} doesn't exist"
        }
    )


async def product_already_exists_handler(
    request: Request,
    exc: ProductAlreadyExistsError
):

    return JSONResponse(
        status_code=409,
        content={
            "message":
                f"Product with item number {exc.item_number} already exists"
        }
    )


async def metrics_not_found_handler(
    request: Request,
    exc: MetricsNotFoundError
):

    return JSONResponse(
        status_code=404,
        content={
            "message":
                f"Metrics with id {exc.metrics_id} don't exist"
        }
    )
