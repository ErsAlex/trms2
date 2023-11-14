from models.models import User

class SystemMessage():
    def __init__(
        self,
        user: User
        ):
        self.user = user
    
    
    
    async def task_created_message(self):
        message = f'Task created by {self.user.user_name} {self.user.email}'
        return message
    
    async def task_updated_message(self):
        message = f'Task updated by {self.user.user_name} {self.user.email}'
        return message
    
    async def user_added_to_task(self):
        message = f'User {self.user.user_name} {self.user.email} assigned to task'
        return message
    
    async def user_revoke_assignment(self):
        message = f'User {self.user.user_name} {self.user.email} assignment revoked' 
        return message