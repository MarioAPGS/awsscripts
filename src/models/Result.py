class Result:
    def __init__(self, success: bool = True, response: dict = {}, message: str = ""):
        self.success = success
        self.response = response
        self.message = message