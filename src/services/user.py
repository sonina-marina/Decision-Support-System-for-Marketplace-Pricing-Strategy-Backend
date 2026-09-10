from src.db.models.user import User
from src.db.repositories.user import UserRepository
from src.services.exceptions import (UserAlreadyExistsError, 
                                     UserNotFoundError)
from src.schemas.user import (UserCreate, UserUpdateFullname,
                              UserUpdatePassword, UserView, 
                              UserList)


class UserService:
    def __init__(self, user_repository: UserRepository):

        self.user_repository = user_repository


    async def create(self, schema: UserCreate) -> UserView:
        
        user = await self.user_repository.get_user_by_email(schema.email)

        if user is not None:
            raise UserAlreadyExistsError(schema.email)

        #TODO
        hash_password = schema.password

        user = User(
            fullname=schema.fullname,
            email=schema.email,
            hash_password=hash_password
        )

        user = await self.user_repository.save(user)

        user = await self.load_user_(user.id)

        return UserView.model_validate(user)


    async def get_by_id(self, id: int) -> UserView:

        user = await self.load_user_(id)

        return UserView.model_validate(user)


    async def get_all(self) -> UserList:

        users = await self.user_repository.get_all()

        return UserList(
            count=len(users),
            items=[UserView.model_validate(user) for user in users]
        )


    async def delete(self, id: int) -> None:
                                                
        user = await self.load_user_(id)
    
        await self.user_repository.delete(user)


    async def change_fullname(self, schema: UserUpdateFullname) -> UserView:

        user = await self.load_user_(schema.id)
        
        user.fullname = schema.new_fullname
        
        user = await self.user_repository.save(user)

        return UserView.model_validate(user)


    async def change_password(self, schema: UserUpdatePassword) -> UserView:

        user = await self.load_user_(schema.id)
        #TODO
        user.hash_password = schema.new_password
        
        user = await self.user_repository.save(user)

        return UserView.model_validate(user)


    async def load_user_(
        self,
        id: int
    ) -> User:

        user = await self.user_repository.get_by_id(id)

        if not user:
            raise UserNotFoundError(id)

        return user
