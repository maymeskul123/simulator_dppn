import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_dashboard(metrics, total_days, market_data=None):
    """Создание визуальной панели результатов"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('DPPN Simulation Results', fontsize=16)
    
    days = range(total_days)
    
    # 1. Распределение богатства
    last_day_balances = metrics["daily_pp_balances"][-1] if metrics["daily_pp_balances"] else []
    axes[0, 0].hist(last_day_balances, bins=20, alpha=0.7, color='skyblue')
    axes[0, 0].set_title('Final Wealth Distribution')
    axes[0, 0].set_xlabel('PP Balance')
    axes[0, 0].set_ylabel('Number of Citizens')
    
    # 2. Коэффициент Джини over time
    axes[0, 1].plot(days, metrics["gini_coefficients"], 'r-', linewidth=2)
    axes[0, 1].set_title('Gini Coefficient Over Time')
    axes[0, 1].set_xlabel('Days')
    axes[0, 1].set_ylabel('Gini Coefficient')
    axes[0, 1].grid(True)
    
    # 3. Уровень счастья
    axes[0, 2].plot(days, metrics["average_happiness"], 'g-', linewidth=2)
    axes[0, 2].set_title('Average Happiness')
    axes[0, 2].set_xlabel('Days')
    axes[0, 2].set_ylabel('Happiness Score')
    axes[0, 2].grid(True)
    
    # 4. Инфляция
    axes[1, 0].plot(days, metrics["inflation_rates"], 'orange', linewidth=2)
    axes[1, 0].set_title('Inflation Rate')
    axes[1, 0].set_xlabel('Days')
    axes[1, 0].set_ylabel('Inflation Rate')
    axes[1, 0].grid(True)
    
    # 5. Образовательный уровень
    axes[1, 1].plot(days, metrics["education_levels"], 'purple', linewidth=2)
    axes[1, 1].set_title('Average Education Level')
    axes[1, 1].set_xlabel('Days')
    axes[1, 1].set_ylabel('Education Level')
    axes[1, 1].grid(True)
    
    # 6. Сравнение начального и конечного распределения
    if len(metrics["daily_pp_balances"]) > 1:
        initial_balances = metrics["daily_pp_balances"][0]
        final_balances = metrics["daily_pp_balances"][-1]
        
        axes[1, 2].hist([initial_balances, final_balances], bins=20, alpha=0.7, 
                       label=['Initial', 'Final'], color=['red', 'blue'])
        axes[1, 2].set_title('Wealth Distribution: Initial vs Final')
        axes[1, 2].legend()
    
    # Новый график - индекс цен рынка
    if market_data and 'price_index' in market_data:
        axes[1, 2].plot(range(len(market_data['price_index'])), market_data['price_index'], 'b-', linewidth=2)
        axes[1, 2].set_title('Market Price Index')
        axes[1, 2].set_xlabel('Days')
        axes[1, 2].set_ylabel('Price Index')
        axes[1, 2].grid(True)
    
    plt.tight_layout()
    plt.savefig('dppn_simulation_results.png', dpi=300, bbox_inches='tight')
    plt.show()