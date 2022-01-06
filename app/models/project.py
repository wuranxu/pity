from sqlalchemy import INT, Column, String, BOOLEAN

from app.models.basic import PityBase


class Project(PityBase):
    __tablename__ = 'pity_project'
    id = Column(INT, primary_key=True)
    name = Column(String(16), unique=True, index=True)
    owner = Column(INT)
    app = Column(String(32), index=True)
    private = Column(BOOLEAN, default=False)
    description = Column(String(200))
    avatar = Column(String(128), nullable=True)

    def __init__(self, name, app, owner, create_user, description="", private=False, avatar=None):
        super().__init__(create_user)
        self.name = name
        self.app = app
        self.owner = owner
        self.private = private
        self.description = description
        self.avatar = avatar
