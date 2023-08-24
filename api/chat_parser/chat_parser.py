from chat_parser.parser_data_classes import Summary, Chat
from DB.models import Groups
from app import db

ERROR_PARSING = "Error while parsing: "
CHAT_ERROR_PARSING = ERROR_PARSING + "Error while parsing specific chat."


class ChatParser:
    def __init__(self, chats_json, user_id: str):
        self.summary = Summary(0, 0, None)
        self.user_id = user_id
        self.chats_json = chats_json

    def parse(self) -> Summary:
        self.chats = self.create_chats()
        created_groups = self.create_db_records(self.chats)
        self.summary = Summary(len(self.chats), len(self.chats_json), self.user_id)

        return self.summary

    def create_chats(self) -> list[Chat]:
        self.chats = []
        for json_chat in self.chats_json:
            try:
                chat = self.create_chat(json_chat)
                self.chats.append(chat)
            except KeyError:
                self.summary.total_records_failed += 1

        self.summary.total_records_created = len(self.chats)

        return self.chats

    def create_chat(self, json_chat: dict) -> Chat:
        try:
            chat = Chat(
                group_id=json_chat.get("id").get("_serialized"),
                group_name=json_chat.get("name"),
                user_id=self.user_id,
            )
        except KeyError:
            raise Exception(CHAT_ERROR_PARSING)

        return chat

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
