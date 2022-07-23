class ProjectRoleEnum:
    MEMBER = 0
    ADMIN = 1

    @staticmethod
    def name(role):
        if role == 1:
            return "组长"
        if role == 0:
            return "组员"
        return None
