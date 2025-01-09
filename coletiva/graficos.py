import re
import matplotlib.pyplot as plt
import numpy as np

# Função para extrair os valores necessários de um arquivo
# Modifique este padrão se a estrutura dos arquivos mudar
def extract_values(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Extrai o tempo total em segundos e converte para minutos
    time_elapsed_match = re.search(r"seconds time elapsed\n\n\s+(\d+\.\d+)", content)
    if time_elapsed_match:
        time_elapsed_minutes = float(time_elapsed_match.group(1)) / 60
    else:
        raise ValueError(f"Tempo total não encontrado no arquivo {filename}")

    # Extrai CPUs utilized
    cpus_utilized_match = re.search(r"#\s+(\d+\.\d+) CPUs utilized", content)
    if cpus_utilized_match:
        cpus_utilized = float(cpus_utilized_match.group(1))
    else:
        raise ValueError(f"CPUs utilized não encontrado no arquivo {filename}")

    # Extrai insn per cycle
    insn_per_cycle_match = re.search(r"#\s+(\d+\.\d+)\s+insn per cycle", content)
    if insn_per_cycle_match:
        insn_per_cycle = float(insn_per_cycle_match.group(1))
    else:
        raise ValueError(f"Insn per cycle não encontrado no arquivo {filename}")

    return time_elapsed_minutes, cpus_utilized, insn_per_cycle

# Nomes dos arquivos para análise
# Substitua por parâmetros para maior flexibilidade futuramente
file_groups = {
    "40_tasks_2_machines": [
        "coletiva_2048_40_2.out",
        "coletiva_8192_40_2.out",
        "coletiva_16384_40_2.out"
    ],
    "80_tasks_2_machines": [
        "coletiva_2048_80_2.out",
        "coletiva_8192_80_2.out",
        "coletiva_16384_80_2.out"
    ],
    "120_tasks_3_machines": [
        "coletiva_2048_120_3.out",
        "coletiva_8192_120_3.out",
        "coletiva_16384_120_3.out"
    ],
    "160_tasks_4_machines": [
        "coletiva_2048_160_4.out",
        "coletiva_8192_160_4.out",
        "coletiva_16384_160_4.out"
    ]
}

# Gráficos
# Modifique "bar" para "line" para trocar entre gráficos de barra e de linha
def plot_comparison(data, metric, title, ylabel):
    x_labels = list(data.keys())
    x_pos = np.arange(len(x_labels))

    # Dados para o gráfico
    values = [data[label][metric] for label in x_labels]

    plt.figure(figsize=(10, 6))

    # Escolha o tipo de gráfico: barra ou linha
    plt.bar(x_pos, values, align='center', alpha=0.7, color='blue')  # Mude para plt.plot para linha
    # plt.plot(x_pos, values, marker='o', linestyle='-', color='blue')

    plt.xticks(x_pos, x_labels, rotation=45)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Arquivos")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# Processar os arquivos e preparar os dados para gráficos
for group_name, files in file_groups.items():
    metrics = {}

    for file in files:
        try:
            time_elapsed, cpus_utilized, insn_per_cycle = extract_values(file)
            metrics[file] = {
                "time_elapsed": time_elapsed,
                "cpus_utilized": cpus_utilized,
                "insn_per_cycle": insn_per_cycle
            }
        except ValueError as e:
            print(e)

    # Gerar gráficos para cada métrica
    plot_comparison(metrics, "time_elapsed", f"Tempo em Minutos ({group_name})", "Tempo (min)")
    plot_comparison(metrics, "cpus_utilized", f"CPUs Utilizadas ({group_name})", "CPUs Utilizadas")
    plot_comparison(metrics, "insn_per_cycle", f"Insn por Ciclo ({group_name})", "Insn/Ciclo")

# Notas:
# 1. Para passar os arquivos como parâmetros, modifique o código para usar sys.argv ou argparse.
# 2. Substitua plt.bar por plt.plot para gráficos de linha.
# 3. Certifique-se de que os arquivos estejam no mesmo diretório ou use caminhos absolutos se necessário.
