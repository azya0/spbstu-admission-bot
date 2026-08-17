class DictDatabaseKeyNotFound(BaseException):
    def __init__(self, key: str) -> None:
        super().__init__(f"DictDatabase not found key: {key}")
