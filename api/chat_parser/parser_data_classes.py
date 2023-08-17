from dataclasses import dataclass


@dataclass
class Summary:
    len_chats_json: int
    user_id: str
    total_records_created: int = 0
    total_records_failed: int = 0

    def __init__(self, len_data_variables, len_chats_json, user_id):
        self.len_chats_json = len_chats_json
        self.user_id = user_id
        self.total_records_created = len_data_variables
        self.total_records_failed = len_chats_json - len_data_variables
