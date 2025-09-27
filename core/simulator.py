import random
from core.citizen import Citizen, AgentType
from core.economy import DPPNEconomy
from models.education import EducationSystem
from models.market import Market
from config.settings import SIMULATION_CONFIG, AGENT_TYPES

class DPPNSimulator:
    def __init__(self, config=None):
        self.config = config or SIMULATION_CONFIG
        self.citizens = []
        self.economy = DPPNEconomy()
        self.education_system = EducationSystem()
        self.market = Market()
        self.day = 0
        self.metrics = {
            "daily_pp_balances": [],
            "gini_coefficients": [],
            "inflation_rates": [],
            "average_happiness": [],
            "education_levels": []
        }
        
    def initialize_population(self):
        """Инициализация населения"""
        agent_types = list(AgentType)
        
        for i in range(self.config["population_size"]):
            agent_type = random.choice(agent_types)
            age = random.randint(18, 80)
            citizen = Citizen(i, agent_type, age)
            
            # Начальный баланс based on type
            base_income = AGENT_TYPES[agent_type.value]["base_income"]
            citizen.pp_balance = random.randint(int(base_income * 0.5), int(base_income * 1.5))
            
            self.citizens.append(citizen)
            
    def run_day(self):
        """Запуск одного дня симуляции (обновленная версия)"""
        # Базовый доход для всех
        for citizen in self.citizens:
            citizen.receive_basic_income(self.config["basic_income_amount"])
        
        # Налоги и перераспределение
        self.economy.redistribute_wealth(self.citizens, self.config["basic_income_amount"])
        
        # Образовательный процесс
        completed_courses = self.education_system.process_education(self.citizens)
        
        # Обновление рыночных условий
        inflation_rate = self.economy.calculate_inflation(self.citizens)
        self.market.update_market_conditions(self.citizens, inflation_rate)
        
        # Экономические решения граждан
        for citizen in self.citizens:
            decisions = citizen.make_economic_decision(self.market)
            self.process_decisions(citizen, decisions)
        
        # Расчет метрик
        self.calculate_metrics()
        self.day += 1
        
    def process_decisions(self, citizen, decisions):
        """Обработка решений граждан"""
        for decision in decisions:
            if decision == "invest_in_education" and citizen.pp_balance > 20:
                # Случайный выбор курса
                course_type = random.choice(list(self.education_system.courses.keys()))
                self.education_system.enroll_student(citizen, course_type)
                
            elif decision == "buy_products":
                # Покупка базовых товаров
                cost = 25
                if citizen.pp_balance >= cost:
                    citizen.pp_balance -= cost
                    citizen.happiness = min(100, citizen.happiness + 5)
        
    def calculate_metrics(self):
        """Расчет и сохранение метрик"""
        balances = [c.pp_balance for c in self.citizens]
        happiness = [c.happiness for c in self.citizens]
        education = [c.education_level for c in self.citizens]
        
        self.metrics["daily_pp_balances"].append(balances)
        self.metrics["gini_coefficients"].append(self.economy.calculate_gini(self.citizens))
        self.metrics["inflation_rates"].append(self.economy.calculate_inflation(self.citizens))
        self.metrics["average_happiness"].append(sum(happiness) / len(happiness))
        self.metrics["education_levels"].append(sum(education) / len(education))
        
    def run_simulation(self, days=None):
        """Запуск полной симуляции"""
        days = days or self.config["simulation_days"]
        
        print(f"Starting DPPN simulation for {days} days...")
        print(f"Population: {len(self.citizens)} citizens")
        
        for day in range(days):
            self.run_day()
            
            if day % 30 == 0:  # Отчет каждый месяц
                self.print_progress(day)
                
        self.print_final_report()
        
    def print_progress(self, day):
        """Печать прогресса симуляции"""
        avg_balance = sum(self.metrics["daily_pp_balances"][-1]) / len(self.citizens)
        avg_happiness = self.metrics["average_happiness"][-1]
        gini = self.metrics["gini_coefficients"][-1]
        
        print(f"Day {day}: Avg PP={avg_balance:.1f}, Happiness={avg_happiness:.1f}, Gini={gini:.3f}")
        
    def print_final_report(self):
        """Финальный отчет симуляции"""
        print("\n" + "="*50)
        print("DPPN SIMULATION FINAL REPORT")
        print("="*50)
        
        final_metrics = {
            "Average PP Balance": sum(self.metrics["daily_pp_balances"][-1]) / len(self.citizens),
            "Final Gini Coefficient": self.metrics["gini_coefficients"][-1],
            "Average Happiness": self.metrics["average_happiness"][-1],
            "Average Education Level": self.metrics["education_levels"][-1],
            "Poverty Rate": self.calculate_poverty_rate()
        }
        
        for metric, value in final_metrics.items():
            print(f"{metric}: {value:.2f}")
            
        # Сравнение с началом симуляции
        initial_gini = self.metrics["gini_coefficients"][0] if self.metrics["gini_coefficients"] else 0.5
        gini_change = ((final_metrics["Final Gini Coefficient"] - initial_gini) / initial_gini) * 100
        
        print(f"\nGini coefficient change: {gini_change:+.1f}%")
        
    def calculate_poverty_rate(self, poverty_line=50):
        """Расчет уровня бедности"""
        poor_citizens = sum(1 for c in self.citizens if c.pp_balance < poverty_line)
        return (poor_citizens / len(self.citizens)) * 100