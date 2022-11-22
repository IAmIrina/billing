from enum import Enum


class HttpMethod(Enum):
    """Класс с перечислением методов HTTP запросов"""
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"