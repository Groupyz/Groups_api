from dataclasses import dataclass

@dataclass
class Summary:
  len_data_variables: int
  len_chats_json: int
  user_id: str

    def __init__(self, len_data_variables, len_chats_json, user_id):
      self.len_data_variables = len_data_variables
      self.len_chats_json = len_chats_json
      self.user_id = user_id