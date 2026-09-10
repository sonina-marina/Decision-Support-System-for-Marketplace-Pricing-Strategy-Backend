from pydantic import EmailStr


class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id


class UserAlreadyExistsError(Exception):
    def __init__(self, email: EmailStr):
        self.email = email


class StoreNotFoundError(Exception):
    def __init__(self, store_id: int):
        self.store_id = store_id


class StoreAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name = name


class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id


class ProductAlreadyExistsError(Exception):
    def __init__(self, item_number: int):
        self.item_number = item_number


class MetricsNotFoundError(Exception):
    def __init__(self, metrics_id: int):
        self.metrics_id = metrics_id


class InvalidCredentialsError(Exception):
    def __init__(self):
        pass


class UnauthorizedError(Exception):
    def __init__(self):
        pass


class ForbiddenError(Exception):
    def __init__(self):
        pass
