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
        }
