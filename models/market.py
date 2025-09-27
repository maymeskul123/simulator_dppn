import random
from typing import Dict, List
from enum import Enum

class ProductCategory(Enum):
    FOOD = "food"
    HOUSING = "housing"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    LUXURY = "luxury"

class Product:
    def __init__(self, product_id: int, name: str, category: ProductCategory, base_price: float, quality: float = 1.0):
        self.id = product_id
        self.name = name
        self.category = category
        self.base_price = base_price
        self.quality = quality
        self.current_price = base_price
        self.demand = 1.0
        self.supply = 1.0
        
    def update_price(self, inflation_rate: float = 0.0):
        """Обновление цены на основе спроса/предложения и инфляции"""
        # Базовая формула цены: base_price * (demand/supply) * (1 + inflation)
        demand_supply_ratio = self.demand / max(self.supply, 0.1)  # Избегаем деления на 0
        price_adjustment = demand_supply_ratio * (1 + inflation_rate)
        
        self.current_price = max(self.base_price * 0.5, self.base_price * price_adjustment)
        return self.current_price
        
    def __repr__(self):
        return f"{self.name} ({self.category.value}): {self.current_price:.1f} PP"

class Market:
    def __init__(self):
        self.products = self.initialize_products()
        self.transactions = []
        self.total_transaction_volume = 0
        self.price_index = 100  # Базовый индекс цен
        
    def initialize_products(self) -> List[Product]:
        """Инициализация базовых товаров и услуг"""
        products = [
            # Еда
            Product(1, "Basic Food Ration", ProductCategory.FOOD, 20.0, 0.8),
            Product(2, "Quality Food Package", ProductCategory.FOOD, 40.0, 1.2),
            Product(3, "Organic Premium Food", ProductCategory.FOOD, 60.0, 1.5),
            
            # Жилье
            Product(4, "Basic Housing", ProductCategory.HOUSING, 100.0, 0.7),
            Product(5, "Comfortable Apartment", ProductCategory.HOUSING, 200.0, 1.3),
            Product(6, "Luxury Residence", ProductCategory.HOUSING, 500.0, 2.0),
            
            # Образование
            Product(7, "Online Course", ProductCategory.EDUCATION, 30.0, 1.0),
            Product(8, "Professional Training", ProductCategory.EDUCATION, 80.0, 1.5),
            Product(9, "University Program", ProductCategory.EDUCATION, 150.0, 2.0),
            
            # Здравоохранение
            Product(10, "Basic Healthcare", ProductCategory.HEALTHCARE, 25.0, 1.0),
            Product(11, "Advanced Medical Care", ProductCategory.HEALTHCARE, 75.0, 1.8),
            Product(12, "Premium Health Package", ProductCategory.HEALTHCARE, 120.0, 2.2),
            
            # Роскошь
            Product(13, "Entertainment", ProductCategory.LUXURY, 50.0, 1.2),
            Product(14, "Luxury Goods", ProductCategory.LUXURY, 100.0, 1.8),
            Product(15, "Exclusive Services", ProductCategory.LUXURY, 200.0, 2.5)
        ]
        return products
        
    def find_affordable_products(self, budget: float, category: ProductCategory = None) -> List[Product]:
        """Поиск товаров, доступных для данного бюджета"""
        affordable = []
        for product in self.products:
            if category and product.category != category:
                continue
            if product.current_price <= budget:
                affordable.append(product)
        
        # Сортировка по качеству (лучшие товары сначала)
        affordable.sort(key=lambda x: x.quality, reverse=True)
        return affordable
        
    def simulate_purchase(self, citizen, product: Product) -> bool:
        """Симуляция покупки товара гражданином"""
        if citizen.pp_balance >= product.current_price:
            # Совершение покупки
            citizen.pp_balance -= product.current_price
            citizen.happiness = min(100, citizen.happiness + product.quality * 5)
            
            # Регистрация транзакции
            transaction = {
                'day': citizen.simulator_day if hasattr(citizen, 'simulator_day') else 0,
                'citizen_id': citizen.id,
                'product_id': product.id,
                'price': product.current_price,
                'category': product.category.value
            }
            self.transactions.append(transaction)
            self.total_transaction_volume += product.current_price
            
            # Обновление спроса на продукт
            product.demand += 0.1
            return True
        return False
        
    def update_market_conditions(self, citizens: List, inflation_rate: float = 0.0):
        """Обновление рыночных условий на основе поведения граждан"""
        
        # Анализ покупательной способности
        total_wealth = sum(c.pp_balance for c in citizens)
        avg_wealth = total_wealth / len(citizens) if citizens else 0
        
        # Обновление спроса на основе благосостояния
        for product in self.products:
            # Базовый спрос зависит от категории товара
            base_demand = self.get_base_demand_for_category(product.category)
            
            # Корректировка спроса на основе благосостояния
            wealth_factor = avg_wealth / 100  # Нормализация
            if product.category == ProductCategory.LUXURY:
                demand_multiplier = max(0, wealth_factor - 1)  # Роскошь покупают при достатке > среднего
            else:
                demand_multiplier = min(1, wealth_factor)  # Базовые товары - при любом достатке
                
            product.demand = base_demand * (1 + demand_multiplier)
            
            # Обновление предложения (упрощенная модель)
            product.supply = 1.0 + (wealth_factor * 0.5)  # Предложение растет с благосостоянием
            
            # Обновление цен
            old_price = product.current_price
            new_price = product.update_price(inflation_rate)
            
            # Логирование значительных изменений цен
            price_change = abs(new_price - old_price) / old_price if old_price > 0 else 0
            if price_change > 0.1:  # Изменение цены более чем на 10%
                print(f"Price alert: {product.name} {old_price:.1f} -> {new_price:.1f} PP")
        
        # Расчет индекса цен
        self.calculate_price_index()
        
    def get_base_demand_for_category(self, category: ProductCategory) -> float:
        """Базовый спрос по категориям товаров"""
        demand_map = {
            ProductCategory.FOOD: 2.0,       # Высокий базовый спрос
            ProductCategory.HOUSING: 1.5,    # Средний спрос
            ProductCategory.EDUCATION: 1.2,  # Растущий спрос в DPPN
            ProductCategory.HEALTHCARE: 1.3, # Стабильный спрос
            ProductCategory.LUXURY: 0.5      # Низкий базовый спрос
        }
        return demand_map.get(category, 1.0)
    
    def calculate_price_index(self) -> float:
        """Расчет индекса потребительских цен"""
        if not self.products:
            return 100.0
            
        total_price = sum(p.current_price for p in self.products)
        avg_price = total_price / len(self.products)
        
        # Упрощенный расчет индекса (в реальности - взвешенный по корзине)
        base_avg_price = sum(p.base_price for p in self.products) / len(self.products)
        self.price_index = (avg_price / base_avg_price) * 100
        
        return self.price_index
    
    def get_market_statistics(self) -> Dict:
        """Получение статистики рынка"""
        category_stats = {}
        
        for category in ProductCategory:
            category_products = [p for p in self.products if p.category == category]
            if category_products:
                avg_price = sum(p.current_price for p in category_products) / len(category_products)
                total_demand = sum(p.demand for p in category_products)
                category_stats[category.value] = {
                    'average_price': avg_price,
                    'total_demand': total_demand,
                    'product_count': len(category_products)
                }
        
        return {
            'price_index': self.price_index,
            'total_products': len(self.products),
            'total_transactions': len(self.transactions),
            'transaction_volume': self.total_transaction_volume,
            'categories': category_stats
        }
    
    def print_market_report(self):
        """Печать отчета о состоянии рынка"""
        stats = self.get_market_statistics()
        
        print("\n" + "="*40)
        print("MARKET REPORT")
        print("="*40)
        print(f"Price Index: {stats['price_index']:.1f}")
        print(f"Total Transactions: {stats['total_transactions']}")
        print(f"Transaction Volume: {stats['transaction_volume']:.1f} PP")
        
        print("\nCategory Statistics:")
        for category, data in stats['categories'].items():
            print(f"  {category.upper():12} | Price: {data['average_price']:6.1f} | Demand: {data['total_demand']:5.1f}")