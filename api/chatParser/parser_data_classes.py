from dataclasses import dataclass


@dataclass
class Chat:
    group_id: str
    group_name: str
    user_id: str

    def __init__(self, group_id, group_name, user_id):
        self.group_id = group_id
        self.group_name = group_name
        self.user_id = user_id
