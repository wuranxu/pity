from app.models import db
from datetime import datetime


class Project(db.Model):
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(16), unique=True, index=True)
    owner = db.Column(db.INT)
    app = db.Column(db.String(32), index=True)
    created_at = db.Column(db.DATETIME, nullable=False)
    updated_at = db.Column(db.DATETIME, nullable=False)
    deleted_at = db.Column(db.DATETIME)
    create_user = db.Column(db.INT, nullable=True)
    update_user = db.Column(db.INT, nullable=True)
    private = db.Column(db.BOOLEAN, default=False)
    description = db.Column(db.String(200))

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
