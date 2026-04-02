import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)
n_notebooks = 1000

data = {
    'id_notebook': range(1, n_notebooks + 1),
    'idade_anos': np.random.randint(1, 6, n_notebooks),
    'tipo_armazenamento': np.random.choice(['HDD', 'SSD'], n_notebooks),
    'ram_gb': np.random.choice([4, 8, 16], n_notebooks)
}

df = pd.DataFrame(data)

def calcular_tempo_base(tipo_armazenamento):
    if tipo_armazenamento == 'HDD':
        return np.random.randint(40, 80)
    else:
        return np.random.randint(10, 20)
    
def calcular_tempo_desgaste(row):
    tipo = row['tipo_armazenamento']
    idade = row['idade_anos']
    base = row['tempo_base']

    if tipo == 'HDD':
        return base * (1.1**idade)
    else:
        return base * (1.05**idade)
        
def calcular_tempo_final(row):
    tempo_desgaste = row['tempo_com_desgaste']
    memoria = row['ram_gb']

    if memoria == 4:
        return tempo_desgaste * 1.2
    elif memoria == 16:
        return tempo_desgaste * 0.9
    else:
        return tempo_desgaste


df['tempo_base'] = df['tipo_armazenamento'].apply(calcular_tempo_base)

df['tempo_com_desgaste'] = df[['tempo_base', 'tipo_armazenamento', 'idade_anos']].apply(calcular_tempo_desgaste, axis=1).round(2)

df['tempo_boot_final'] = df[['ram_gb', 'tempo_com_desgaste']].apply(calcular_tempo_final, axis=1).round(2)

plt.figure(figsize=(12,6))
sns.boxplot(data=df, x='idade_anos', y='tempo_boot_final', hue='tipo_armazenamento', palette='viridis')
plt.title("Degradação de performace: HDD vs SSD (1 a 5 anos)")
plt.ylabel("Tempo de Boot (Segundos)")
plt.xlabel("Idade do Equipamento (Anos)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('boxplot_performance.png', bbox_inches='tight', dpi=300)
plt.show()


plt.figure(figsize=(12,6))
sns.lineplot(data=df, x='ram_gb', y='tempo_boot_final', hue='tipo_armazenamento' ,linewidth=2.5, marker='o', palette='Set1')
plt.title("Análise de performace combinada: Memória RAM influência no tempo de boot?")
plt.ylabel("Tempo de Boot (Segundos)")
plt.xlabel("Memória RAM (GB)")
plt.xticks([4, 8, 16])
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('lineplot_performance.png', bbox_inches='tight', dpi=300)
plt.show()