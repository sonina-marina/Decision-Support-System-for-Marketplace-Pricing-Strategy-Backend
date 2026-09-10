from src.schemas.metric import ProductCalculationData, MetricsResult


class MetricCalculator():

    @classmethod
    def _calculate_conversion(cls, product: ProductCalculationData) -> float:
        if product.views <= 0:
            raise ValueError(
                "Количество просмотров должно быть больше нуля."
            )
        return product.target_actions / product.views


    @classmethod
    def _calculate_cac(cls, product: ProductCalculationData) -> float:
        if product.buyers <= 0:
            raise ValueError(
                "Количество покупателей должно быть больше нуля."
            )
        return product.ad_costs / product.buyers

    
    @classmethod
    def _calculate_required_cpa(cls, product: ProductCalculationData) -> float:
        if product.target_actions <= 0:
            raise ValueError(
                "Количество целевых действий должно быть больше нуля."
            )

        return product.ad_costs / product.target_actions


    @classmethod
    def _calculate_ltc(cls, product: ProductCalculationData) -> float:
        return (product.cogs +
               product.price * product.commission / 100 +
               product.price * product.acquiring / 100 + 
               product.price * product.tax / 100 +
               product.inbound_logistic +
               product.direct_logistic +
               product.return_rate * product.reverse_logistic +
               product.cogs * product.return_rate * product.defect_rate + #испорченные среди возвратов, теряем себестоимость
               product.avg_storage +
               product.avg_packaging)


    @classmethod
    def _calculate_cm(cls, product: ProductCalculationData, ltc) -> float:
        return product.price - ltc


    @classmethod
    def _calculate_ltv(cls, product: ProductCalculationData, cm) -> float:
        if product.buyers <= 0:
            raise ValueError(
                "Количество покупателей должно быть больше нуля."
            )
        return cm * product.sales / product.buyers


    @classmethod
    def _calculate_product_roi(cls, cm, ltc) -> float:
        if ltc <= 0:
            raise ValueError(
                "Затраты должны быть больше нуля."
            )
        return cm / ltc * 100


    @classmethod
    def calculate(cls, product: ProductCalculationData):

        conversion = cls._calculate_conversion(product)

        cac = cls._calculate_cac(product)

        required_cpa = cls._calculate_required_cpa(product)

        ltc = cls._calculate_ltc(product)

        cm = cls._calculate_cm(product, ltc=ltc)

        ltv = cls._calculate_ltv(product, cm=cm)

        product_roi = cls._calculate_product_roi(cm=cm, ltc=ltc)

        return MetricsResult(
            conversion=conversion,
            cac=cac,
            required_cpa=required_cpa,
            ltc=ltc,
            cm=cm,
            ltv=ltv,
            product_roi=product_roi
        )


