from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .operation_result import OperationResult

db = SQLAlchemy()
migrate = Migrate()
