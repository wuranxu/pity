from datetime import datetime

from sqlalchemy import INT, Column, DATETIME

from app.models import Base


class ProjectRole(Base):
    __tablename__ = 'pity_project_role'
    id = Column(INT, primary_key=True)
    user_id = Column(INT, index=True)
    project_id = Column(INT, index=True)
    project_role = Column(INT, index=True)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    create_user = Column(INT, nullable=True)
    update_user = Column(INT, nullable=True)

    def __init__(self, user_id, project_id, project_role, create_user):
        self.user_id = user_id
        self.project_id = project_id
        self.project_role = project_role
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = create_user
        self.update_user = create_user
        self.deleted_at = None
