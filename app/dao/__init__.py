from app.models import Base, engine
from app.models.user import User
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.models.test_case import TestCase
from app.models.testcase_asserts import TestCaseAsserts
from app.models.environment import Environment
from app.models.gconfig import GConfig
from app.models.constructor import Constructor
from app.models.report import PityReport
from app.models.result import PityTestResult
from app.models.database import PityDatabase
from app.models.testcase_directory import PityTestcaseDirectory
from app.models.testcase_data import PityTestcaseData
from app.models.test_plan import PityTestPlan

Base.metadata.create_all(engine)
