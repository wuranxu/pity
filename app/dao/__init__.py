from app.models import Base, engine
from app.models.user import User
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.models.test_case import TestCase
from app.models.testcase_asserts import TestCaseAsserts
from app.models.environment import Environment
from app.models.gconfig import GConfig

Base.metadata.create_all(engine)
