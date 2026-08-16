class UnexpectedStatus(BaseException):
    def __init__(self, status_code: int, body: str):
        super().__init__(f"Unexpected status code: {status_code} with body:\n\n{body}")
