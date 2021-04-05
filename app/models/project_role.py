from app.models import db
from datetime import datetime


class ProjectRole(db.Model):
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.INT, index=True)
    project_id = db.Column(db.INT, index=True)
    project_role = db.Column(db.INT, index=True)
    created_at = db.Column(db.DATETIME, nullable=False)
    updated_at = db.Column(db.DATETIME, nullable=False)
    deleted_at = db.Column(db.DATETIME)
    create_user = db.Column(db.INT, nullable=True)
    update_user = db.Column(db.INT, nullable=True)

    def __init__(self, user_id, project_id, project_role, create_user):
        self.user_id = user_id
        self.project_id = project_id
        self.project_role = project_role
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.create_user = create_user
        self.update_user = create_user
        self.deleted_at = None
