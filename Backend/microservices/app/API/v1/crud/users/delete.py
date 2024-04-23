from pydantic import BaseModel

class UserDelete:
    
    class structure(BaseModel):
        user_id: str
    
    def __init__(self, raw_data: structure) -> None:
        user_id = raw_data["user_id"]

        self.response = self.remove(user_id)

    def remove(self, user_id):
        pass