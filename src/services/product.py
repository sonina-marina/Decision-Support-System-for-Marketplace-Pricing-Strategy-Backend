from src.db.models.product import Product
from src.db.repositories.product import ProductRepository
from src.db.repositories.metrics import MetricsRepository
from src.schemas.metrics import MetricsView
from src.schemas.product import (ProductCreate, ProductDetailedView, 
                                 ProductList, ProductUpdate, ProductView)
from src.services.exceptions import (ProductAlreadyExistsError,
                                     ProductNotFoundError)


class ProductService:
    def __init__(
            self,
            product_repository: ProductRepository,
            metrics_repository: MetricsRepository
        ):

        self.product_repository = product_repository
        self.metrics_repository = metrics_repository


    async def create(self, schema: ProductCreate) -> ProductView:

        product = await self.product_repository.get_product_by_item_number(schema.item_number)

        if product is not None:
            raise ProductAlreadyExistsError(schema.item_number)

        product = Product(
            shop_id=schema.shop_id,
            item_number=schema.item_number,
            name=schema.name,
            category=schema.category,
            
            price=schema.price,
            cogs=schema.cogs,
            commission=schema.commission,
            acquiring=schema.acquiring,
            tax=schema.tax,

            views=schema.views,
            target_actions=schema.target_actions,
            buyers=schema.buyers,

            ad_costs=schema.ad_costs,

            inbound_logistic=schema.inbound_logistic,
            direct_logistic=schema.direct_logistic,
            reverse_logistic=schema.reverse_logistic,

            return_rate=schema.return_rate,
            defect_rate=schema.defect_rate,

            avg_storage=schema.avg_storage,
            avg_packaging=schema.avg_packaging,

            sales=schema.sales
        )

        product = await self.product_repository.save(product)

        product = await self.load_product_(product.id)

        return ProductView.model_validate(product)


    async def get_by_id(self, id: int) -> ProductView:

        product = await self.product_repository.get_by_id(id)
        
        if product is None:
            raise ProductNotFoundError(id)

        return ProductView.model_validate(product)


    async def get_all(self) -> ProductList:

        products = await self.product_repository.get_all()

        return ProductList(
            count=len(products),
            items=[ProductView.model_validate(product) for product in products]
        )


    async def get_product_with_metric_by_id(self, id: int) -> ProductDetailedView:

        product = await self.product_repository.get_by_id(id)

        if product is None:
            raise ProductNotFoundError(id)

        metrics = await self.metrics_repository.get_metrics_by_product_id(product.id)

        product_data = product.__dict__.copy()
        product_data.pop('_sa_instance_state', None)

        metrics_views = [MetricsView.model_validate(m, from_attributes=True) for m in metrics]

        return ProductDetailedView(
            **product_data,
            metrics=metrics_views
        )


    async def delete(self, id: int) -> None:
        
        product = await self.product_repository.get_by_id(id)
        
        if product is None:
            raise ProductNotFoundError(id)
    
        await self.product_repository.delete(product)


    async def update(self, schema: ProductUpdate) -> ProductView:

        product = await self.product_repository.get_by_id(schema.id)
        if product is None:
            raise ProductNotFoundError(schema.id)

        product.name=schema.name
        product.category=schema.category
            
        product.price=schema.price
        product.cogs=schema.cogs
        product.commission=schema.commission
        product.acquiring=schema.acquiring
        product.tax=schema.tax

        product.views=schema.views
        product.target_actions=schema.target_actions
        product.buyers=schema.buyers

        product.ad_costs=schema.ad_costs

        product.inbound_logistic=schema.inbound_logistic
        product.direct_logistic=schema.direct_logistic
        product.reverse_logistic=schema.reverse_logistic

        product.return_rate=schema.return_rate
        product.defect_rate=schema.defect_rate

        product.avg_storage=schema.avg_storage
        product.avg_packaging=schema.avg_packaging

        product.sales=schema.sales
        

        product = await self.product_repository.save(product)

        return ProductView.model_validate(product)


    async def load_product_(
        self,
        id: int
    ) -> Product:

        product = await self.product_repository.get_by_id(id)

        if not product:
            raise ProductNotFoundError(id)

        return product
