from core.simulator import DPPNSimulator
from visualization.dashboard import create_dashboard
import matplotlib.pyplot as plt

def main():
    # Создание и запуск симуляции
    simulator = DPPNSimulator()
    simulator.initialize_population()
    
    print("DPPN Simulator v1.0")
    print("Initializing simulation...")
    
    # Короткая симуляция для теста
    simulator.run_simulation(days=90)  # 3 месяца
    
    # Визуализация результатов
    create_dashboard(simulator.metrics, simulator.day)
    
    # Сохранение данных для анализа
    save_simulation_data(simulator)

def save_simulation_data(simulator):
    """Сохранение данных симуляции"""
    import json
    import csv
    
    # Сохранение метрик в JSON
    with open('simulation_results.json', 'w') as f:
        json.dump(simulator.metrics, f, indent=2)
        
    # Сохранение финального состояния граждан в CSV
    with open('citizens_final_state.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Type', 'PP_Balance', 'Education', 'Happiness'])
        
        for citizen in simulator.citizens:
            writer.writerow([
                citizen.id, 
                citizen.agent_type.value,
                citizen.pp_balance,
                citizen.education_level,
                citizen.happiness
            ])
    
    print("Simulation data saved to 'simulation_results.json' and 'citizens_final_state.csv'")

if __name__ == "__main__":
    main()