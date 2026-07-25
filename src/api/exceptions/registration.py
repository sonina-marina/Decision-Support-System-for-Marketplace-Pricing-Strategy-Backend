from fastapi import FastAPI

from src.api.exceptions.handlers import (metrics_not_found_handler, 
                                         product_already_exists_handler, 
                                         product_not_found_handler, 
                                         store_already_exists_handler, 
                                         store_not_found_handler, 
                                         user_atready_exists_handler, 
                                         user_not_found_handler)
from src.services.exceptions import (MetricsNotFoundError, 
                                     ProductAlreadyExistsError, 
                                     ProductNotFoundError, 
                                     StoreAlreadyExistsError, 
                                     StoreNotFoundError, 
                                     UserAlreadyExistsError, 
                                     UserNotFoundError)


def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        UserNotFoundError,
        user_not_found_handler
    )


    app.add_exception_handler(
        UserAlreadyExistsError,
        user_atready_exists_handler
    )


    app.add_exception_handler(
        StoreNotFoundError,
        store_not_found_handler
    )


    app.add_exception_handler(
        StoreAlreadyExistsError,
        store_already_exists_handler
    )


    app.add_exception_handler(
        ProductNotFoundError,
        product_not_found_handler
    )


    app.add_exception_handler(
        ProductAlreadyExistsError,
        product_already_exists_handler
    )


    app.add_exception_handler(
        MetricsNotFoundError,
        metrics_not_found_handler
    )
