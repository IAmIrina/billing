from enum import Enum


class HttpMethod(Enum):
    """Класс с перечислением методов HHTP запросов"""
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"