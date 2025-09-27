from flask import jsonify, Response


class OperationResult:
    def __init__(self, success: bool, message: str, data=None):
        self.success = success
        self.message = message
        self.data = data

    def to_json_response(
        self, success_status_code: int = 200, failed_status_code: int = 400
    ) -> Response:
        return (
            jsonify(self.__dict__),
            success_status_code if self.success else failed_status_code,
            {"Content-Type": "application/json"},
        )
