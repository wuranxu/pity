from app.models import Base
from datetime import datetime
from sqlalchemy import INT, DATETIME, Column, String, BOOLEAN


class Project(Base):
    __tablename__ = 'pity_project'
    id = Column(INT, primary_key=True)
    name = Column(String(16), unique=True, index=True)
    owner = Column(INT)
    app = Column(String(32), index=True)
    created_at = Column(DATETIME, nullable=False)
    updated_at = Column(DATETIME, nullable=False)
    deleted_at = Column(DATETIME)
    create_user = Column(INT, nullable=True)
    update_user = Column(INT, nullable=True)
    private = Column(BOOLEAN, default=False)
    description = Column(String(200))

    def __init__(self, name, app, owner, create_user, description="", private=False):
        self.name = name
        self.app = app
        self.owner = owner
        self.private = private
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = create_user
        self.update_user = create_user
        self.description = description
        self.deleted_at = None
