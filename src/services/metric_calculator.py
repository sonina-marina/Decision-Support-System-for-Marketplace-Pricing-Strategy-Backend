from schemas.metric import ProductCalculationData, MetricsResult


class MetricCalculator():

    def calculate_conversion(self, product: ProductCalculationData) -> float:
        if product.views <= 0:
            raise ValueError(
                "Количество просмотров должно быть больше нуля."
            )
        return product.target_actions / product.views


    def calculate_cac(self, product: ProductCalculationData) -> float:
        if product.buyers <= 0:
            raise ValueError(
                "Количество покупателей должно быть больше нуля."
            )
        return product.ad_costs / product.buyers


    def calculate_required_cpa(self, product: ProductCalculationData) -> float:
        if product.target_actions <= 0:
            raise ValueError(
                "Количество целевых действий должно быть больше нуля."
            )

        return product.ad_costs / product.target_actions

    
    def calculate_ltc(self, product: ProductCalculationData) -> float:
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


    def calculate_cm(self, product: ProductCalculationData, ltc) -> float:
        return product.price - ltc


    def calculate_ltv(self, product: ProductCalculationData, cm) -> float:
        if product.buyers <= 0:
            raise ValueError(
                "Количество покупателей должно быть больше нуля."
            )
        return cm * product.sales / product.buyers


    def calculate_product_roi(self, cm, ltc) -> float:
        if ltc <= 0:
            raise ValueError(
                "Затраты должны быть больше нуля."
            )
        return cm / ltc * 100


    def calculate(self, product):

        conversion = self.calculate_conversion(product)

        cac = self.calculate_cac(product)

        required_cpa = self.calculate_required_cpa(product)

        ltc = self.calculate_ltc(product)

        cm = self.calculate_cm(product, ltc=ltc)

        ltv = self.calculate_ltv(product, cm=cm)

        product_roi = self.calculate_product_roi(cm=cm, ltc=ltc)

        return MetricsResult(
            conversion=conversion,
            cac=cac,
            required_cpa=required_cpa,
            ltc=ltc,
            cm=cm,
            ltv=ltv,
            product_roi=product_roi
        )


