from datetime import datetime

class DiscountStrategy:
    def apply(self, price: float) -> float:
        raise NotImplementedError
    
class NoDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price
    
class SeasonalDiscount(DiscountStrategy):
    def __init__(self, discounts: dict[int, float]):
        self.discounts = discounts
    def apply(self, price:float) -> float:
        current_month = datetime.now().month
        if current_month in self.discounts:
            return price * (1 - self.discounts[current_month])
        return price