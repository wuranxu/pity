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
    dingtalk_url = Column(String(128), nullable=True)
    __tag__ = "项目"
    __fields__ = (name, owner, app, private, description, avatar, dingtalk_url)
    __alias__ = dict(name="项目名称", owner="项目所有者", app="项目所属应用", private="是否私有", description="项目描述", avatar="项目头像",
                     dingtalk_url="钉钉通知url")
    __show__ = 2

    def __init__(self, name, app, owner, create_user, description="", private=False, avatar=None, dingtalk_url=None):
        super().__init__(create_user)
        self.name = name
        self.app = app
        self.owner = owner
        self.private = private
        self.description = description
        self.avatar = avatar
        self.dingtalk_url = dingtalk_url
