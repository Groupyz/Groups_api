from chat_parser.parser_data_classes import Summary


class ChatParser:
    def __init__(self, chats_json, user_id):
        self.summary = Summary(0, 0, None)
