class DPPNEconomy:
    def __init__(self):
        self.total_pp_supply = 0
        self.circulating_pp = 0
        self.tax_revenue = 0
        self.public_funds = 0
        self.day = 0
        self.inflation_rate = 0.0
        self.gdp = 0
        self.gini_coefficient = 0.5
        
    def calculate_inflation(self, citizens):
        """Расчет инфляции на основе роста денежной массы"""
        total_balance = sum(citizen.pp_balance for citizen in citizens)
        money_supply_growth = (total_balance - self.circulating_pp) / self.circulating_pp if self.circulating_pp > 0 else 0
        
        # Инфляция = рост денежной массы - рост экономики
        economic_growth = self.calculate_economic_growth(citizens)
        self.inflation_rate = max(0, money_supply_growth - economic_growth)
        
        self.circulating_pp = total_balance
        return self.inflation_rate
        
    def calculate_economic_growth(self, citizens):
        """Расчет экономического роста на основе человеческого капитала"""
        total_human_capital = sum(citizen.education_level * citizen.health / 100 for citizen in citizens)
        growth = total_human_capital / len(citizens) * 0.01
        return growth
        
    def calculate_gini(self, citizens):
        """Расчет коэффициента Джини (неравенство)"""
        balances = sorted([c.pp_balance for c in citizens])
        n = len(balances)
        cumulative_balance = 0
        cumulative_population = 0
        gini_numerator = 0
        
        for i, balance in enumerate(balances):
            cumulative_balance += balance
            cumulative_population += 1
            gini_numerator += cumulative_balance / sum(balances) - cumulative_population / n
            
        self.gini_coefficient = gini_numerator / n
        return self.gini_coefficient
    
    def redistribute_wealth(self, citizens, basic_income_amount):
        """Перераспределение богатства через базовый доход и налоги"""
        total_tax_revenue = 0
        
        for citizen in citizens:
            # Сбор налогов
            tax_paid = citizen.pay_taxes(0.1)  # 10% налог
            total_tax_revenue += tax_paid
            
            # Выплата базового дохода
            citizen.receive_basic_income(basic_income_amount)
            
        self.tax_revenue = total_tax_revenue
        self.public_funds = total_tax_revenue