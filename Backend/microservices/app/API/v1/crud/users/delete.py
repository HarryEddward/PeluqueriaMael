from pydantic import BaseModel
import numba as nb

class UserDelete:
    
    class structure(BaseModel):
        user_id: str
    
    #@nb.jit(nopython=True)
    def __init__(self, raw_data: structure) -> None:
        user_id = raw_data["user_id"]

        self.response = self.remove(user_id)

    #@nb.jit(nopython=True)
    def remove(self, user_id):
        pass