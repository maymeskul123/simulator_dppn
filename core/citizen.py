import random
from enum import Enum

class AgentType(Enum):
    WORKER = "worker"
    ENTREPRENEUR = "entrepreneur" 
    STUDENT = "student"
    RETIREE = "retiree"

class Citizen:
    def __init__(self, citizen_id, agent_type, age=25):
        self.id = citizen_id
        self.agent_type = agent_type
        self.age = age
        self.pp_balance = 100  # Стартовый баланс
        self.education_level = random.randint(1, 10)
        self.health = 100
        self.happiness = 50
        self.products = []
        self.skills = []
        self.employment_status = "unemployed"
        
        # Характеристики based on type
        self.risk_tolerance = random.uniform(0.1, 0.9)
        self.learning_ability = random.uniform(0.3, 1.0)
        
    def receive_basic_income(self, amount):
        """Получение базового дохода"""
        self.pp_balance += amount
        self.happiness = min(100, self.happiness + 5)
        
    def pay_taxes(self, tax_rate):
        """Уплата налогов"""
        tax_amount = self.pp_balance * tax_rate
        self.pp_balance -= tax_amount
        return tax_amount
        
    def make_economic_decision(self, market):
        """Принятие экономических решений (расширенная версия)"""
        decisions = []
        
        # Базовые потребности (всегда приоритет)
        basic_needs_cost = 45  # Еда + базовое жилье
        if self.pp_balance > basic_needs_cost:
            decisions.append("buy_products")
        
        # Образовательные инвестиции (зависит от склонности к обучению)
        if (self.pp_balance > 50 and self.education_level < 8 and 
            random.random() < self.learning_ability * 0.3):
            decisions.append("invest_in_education")
        
        # Роскошь (только при достаточном богатстве)
        if (self.pp_balance > 150 and self.risk_tolerance > 0.5 and
            random.random() < 0.2):  # 20% шанс
            decisions.append("buy_luxury")
            
        return decisions
    
    def update_education(self, education_system):
        """Обновление образовательного уровня"""
        if self.education_level < 10:
            self.education_level += self.learning_ability * 0.1
            
    def __repr__(self):
        return f"Citizen {self.id} ({self.agent_type.value}): PP={self.pp_balance}, Edu={self.education_level}"