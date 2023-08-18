from chat_parser.parser_data_classes import Summary, Chat
from DB.models import Groups
from app import db


class ChatParser:
    def __init__(self, chats_json, user_id: str):
        self.summary = Summary(0, 0, None)

    def create_db_records(self, chats: list[Chat]) -> list[Groups]:
        groups = []
        for chat in chats:
            group = Groups(
                user_id=chat.user_id, group_id=chat.group_id, group_name=chat.group_name
            )
            groups.append(group)

        db.session.add_all(groups)
        db.session.commit()

        return groups
