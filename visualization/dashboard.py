import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_dashboard(metrics, total_days):
    """Создание визуальной панели результатов"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('DPPN Simulation Results', fontsize=16)
    
    days = range(min(total_days, len(metrics["average_happiness"])))
    
    # 1. Распределение богатства
    if metrics["daily_pp_balances"]:
        last_day_balances = metrics["daily_pp_balances"][-1]
        axes[0, 0].hist(last_day_balances, bins=20, alpha=0.7, color='skyblue')
        axes[0, 0].set_title('Final Wealth Distribution')
        axes[0, 0].set_xlabel('PP Balance')
        axes[0, 0].set_ylabel('Number of Citizens')
    
    # 2. Коэффициент Джини over time
    if metrics["gini_coefficients"]:
        axes[0, 1].plot(days, metrics["gini_coefficients"][:len(days)], 'r-', linewidth=2)
        axes[0, 1].set_title('Gini Coefficient Over Time')
        axes[0, 1].set_xlabel('Days')
        axes[0, 1].set_ylabel('Gini Coefficient')
        axes[0, 1].grid(True)
    
    # 3. Уровень счастья
    if metrics["average_happiness"]:
        axes[0, 2].plot(days, metrics["average_happiness"][:len(days)], 'g-', linewidth=2)
        axes[0, 2].set_title('Average Happiness')
        axes[0, 2].set_xlabel('Days')
        axes[0, 2].set_ylabel('Happiness Score')
        axes[0, 2].grid(True)
    
    # 4. Инфляция
    if metrics["inflation_rates"]:
        axes[1, 0].plot(days, metrics["inflation_rates"][:len(days)], 'orange', linewidth=2)
        axes[1, 0].set_title('Inflation Rate')
        axes[1, 0].set_xlabel('Days')
        axes[1, 0].set_ylabel('Inflation Rate')
        axes[1, 0].grid(True)
    
    # 5. Образовательный уровень
    if metrics["education_levels"]:
        axes[1, 1].plot(days, metrics["education_levels"][:len(days)], 'purple', linewidth=2)
        axes[1, 1].set_title('Average Education Level')
        axes[1, 1].set_xlabel('Days')
        axes[1, 1].set_ylabel('Education Level')
        axes[1, 1].grid(True)
    
    # 6. Индекс цен рынка
    if metrics.get("market_data"):
        price_index = [data.get('price_index', 100) for data in metrics["market_data"]]
        if len(price_index) >= len(days):
            axes[1, 2].plot(days, price_index[:len(days)], 'b-', linewidth=2)
            axes[1, 2].set_title('Market Price Index')
            axes[1, 2].set_xlabel('Days')
            axes[1, 2].set_ylabel('Price Index')
            axes[1, 2].grid(True)
    
    plt.tight_layout()
    plt.savefig('dppn_simulation_results.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_market_dashboard(metrics):
    """Создание отдельной панели для данных рынка"""
    if not metrics.get("market_data"):
        return
        
    market_data = metrics["market_data"]
    days = range(len(market_data))
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('DPPN Market Analysis', fontsize=16)
    
    # 1. Индекс цен
    price_index = [data.get('price_index', 100) for data in market_data]
    axes[0, 0].plot(days, price_index, 'b-', linewidth=2)
    axes[0, 0].set_title('Market Price Index')
    axes[0, 0].set_xlabel('Days')
    axes[0, 0].grid(True)
    
    # 2. Объем транзакций
    transaction_volume = [data.get('transaction_volume', 0) for data in market_data]
    axes[0, 1].plot(days, transaction_volume, 'g-', linewidth=2)
    axes[0, 1].set_title('Daily Transaction Volume')
    axes[0, 1].set_xlabel('Days')
    axes[0, 1].grid(True)
    
    # 3. Спрос по категориям (последний день)
    if market_data and 'categories' in market_data[-1]:
        categories = market_data[-1]['categories']
        category_names = list(categories.keys())
        demands = [categories[cat]['total_demand'] for cat in category_names]
        
        axes[1, 0].bar(category_names, demands, alpha=0.7)
        axes[1, 0].set_title('Demand by Category (Final Day)')
        axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Цены по категориям (последний день)
    if market_data and 'categories' in market_data[-1]:
        categories = market_data[-1]['categories']
        category_names = list(categories.keys())
        prices = [categories[cat]['average_price'] for cat in category_names]
        
        axes[1, 1].bar(category_names, prices, alpha=0.7, color='orange')
        axes[1, 1].set_title('Average Prices by Category (Final Day)')
        axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('dppn_market_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()