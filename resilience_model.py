import numpy as np
import pandas as pd

class BeanResilienceSim:
    """
    Моделирование генетической устойчивости Phaseolus vulgaris к ионизирующему излучению.
    Основано на данных полевых исследований (МНС) и теоретических нормах МАГАТЭ.
    """
    def __init__(self, variety_name="Phoenix_Alpha"):
        self.variety = variety_name
        # LD50 для фасоли обычно колеблется в районе 80-150 Грей (8000-15000 Р)
        self.ld50_gy = 100 

    def calculate_survival(self, dose_r):
        """
        Рассчитывает процент выживаемости. 
        Конвертируем Рентген в Грей (1 Gy = 100 R).
        """
        dose_gy = dose_r / 100
        # Линейно-квадратичная модель выживаемости S = exp(-(alpha*D + beta*D^2))
        alpha = 0.02
        beta = 0.0001
        survival_fraction = np.exp(-(alpha * dose_gy + beta * (dose_gy**2)))
        return max(0, survival_fraction)

    def simulate_mutations(self, dose_r):
        """
        Определяет спектр мутаций в поколении M2.
        """
        if dose_r < 1000:
            return "Stable Genome"
        
        # Чем выше доза, тем выше риск летальных мутаций, 
        # но и выше шанс уникальных морфологических изменений.
        mutation_chance = dose_r / 6000
        roll = np.random.random()
        
        if roll < mutation_chance:
            return np.random.choice([
                "Chlorophyll mutation (Albina/Xantha)", 
                "Dwarfism (Resilient phenotype)", 
                "Early maturity (Strategic advantage)",
                "Increased anthocyanin (Seed color change)",
                "Pod structure modification"
            ])
        return "Wild Type"

def run_armageddon_scenario():
    sim = BeanResilienceSim()
    
    # Контрольные точки: 0, 1000, 2500, 5000, 5600 Рентген
    test_doses = [0, 1000, 2500, 5000, 5600]
    results = []

    print(f"--- Simulation for {sim.variety} ---")
    for dose in test_doses:
        survival = sim.calculate_survival(dose)
        mutation = sim.simulate_mutations(dose)
        results.append({
            "Dose_R": dose,
            "Survival_Rate": f"{survival:.2%}",
            "M2_Mutation_Sample": mutation
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    
    # Сохраняем для отчета
    df.to_csv("survival_report.csv", index=False)
    print("\n[INFO] Report saved as survival_report.csv")

if __name__ == "__main__":
    run_armageddon_scenario()
