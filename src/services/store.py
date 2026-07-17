from sqlalchemy.exc import IntegrityError
from src.db.models.store import Store
from src.db.repositories.store import StoreRepository
from src.schemas.store import (StoreCreate, StoreView, 
                               StoreList, StoreUpdate)
from src.services.exceptions import (StoreAlreadyExistsError,
                                     StoreNotFoundError)

class StoreService:
    def __init__(self, store_repository: StoreRepository):

        self.store_repository = store_repository


    async def create(self, schema: StoreCreate) -> StoreView:
        
        stores = await self.store_repository.get_store_by_user_id(schema.user_id)

        for store in stores:
            if store.name == schema.name:
                raise StoreAlreadyExistsError(schema.name)

        store = Store(
            user_id=schema.user_id,
            name=schema.name
        )

        store = await self.store_repository.save(store)

        store = await self.load_store_(store.id)

        return StoreView.model_validate(store)


    async def get_by_id(self, id: int) -> StoreView:

        store = await self.store_repository.get_by_id(id)
        
        if store is None:
            raise StoreNotFoundError(id)

        return StoreView.model_validate(store)


    async def get_all(self) -> StoreList:

        stores = await self.store_repository.get_all()

        return StoreList(
            count=len(stores),
            items=[StoreView.model_validate(store) for store in stores]
        )


    async def delete(self, id: int) -> None:
        
        store = await self.store_repository.get_by_id(id)
        
        if store is None:
            raise StoreNotFoundError(id)

        await self.store_repository.delete(store)
    

    async def update(self, schema: StoreUpdate) -> StoreView:

        try:
            store = await self.store_repository.get_by_id(schema.id)

            if store is None:
                raise StoreNotFoundError(schema.id)

            store.name = schema.name

            store = await self.store_repository.save(store)
        except IntegrityError:
            raise StoreAlreadyExistsError(schema.name)

        return StoreView.model_validate(store)


    async def load_store_(
        self,
        id: int
    ) -> Store:

        store = await self.store_repository.get_by_id(id)

        if not store:
            raise StoreNotFoundError(id)

        return store
