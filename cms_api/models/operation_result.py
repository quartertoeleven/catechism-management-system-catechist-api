class OperationResult:
    def __init__(self, success: bool, message: str, data = None):
        self.success = success
        self.message = message
        self.data = data