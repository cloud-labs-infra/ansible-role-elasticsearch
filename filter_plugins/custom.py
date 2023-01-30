__author__ = "dale mcdiarmid"

def extract_role_users(users={}, exclude_users=[]):
    role_users = []
    for user, details in list(users.items()):
        if user not in exclude_users and "roles" in details:
            for role in details["roles"]:
                role_users.append(role + ":" + user)
    return role_users


def filter_reserved(users_role={}):
    reserved = []
    for user_role, details in list(users_role.items()):
        if (
                "metadata" in details
                and "_reserved" in details["metadata"]
                and details["metadata"]["_reserved"]
        ):
            reserved.append(user_role)
    return reserved


class FilterModule(object):
    def filters(self):
        return {
            "filter_reserved": filter_reserved,
            "extract_role_users": extract_role_users,
        }
