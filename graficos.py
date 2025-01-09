import re
import matplotlib.pyplot as plt
import numpy as np

# Função para extrair os valores necessários de um arquivo
# Modifique este padrão se a estrutura dos arquivos mudar
def extract_values(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Extrai o tempo total em segundos e converte para minutos
    time_elapsed_match = re.search(r"\s+(\d+\.\d+) seconds time elapsed", content)
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
    "20_tasks_nao_bloqueante": {
        "2_machines": [
        "naobloqueante/naobloqueante_2048_20_2.out"
        ],
        "3_machines": [
        "naobloqueante/naobloqueante_2048_20_3.out"
        ],
        "4_machines": [
        "naobloqueante/naobloqueante_2048_20_4.out"
        ]
    },

    "40_tasks_2_machines": {
        "coletiva": [
        "coletiva/coletiva_2048_40_2.out",
        "coletiva/coletiva_8192_40_2.out",
        "coletiva/coletiva_16384_40_2.out"
    ],
        "bloqueante": [
        "bloqueante/bloquante_2048_40_2.out",
        "bloqueante/bloquante_8192_40_2.out",
        "bloqueante/bloquante_16384_40_2.out"
    ],
        "nao_bloquante": [
        "naobloqueante/naobloqueante_2048_40_2.out",
        "naobloqueante/naobloqueante_8192_40_2.out",
        "naobloqueante/naobloqueante_16384_40_2.out"
    ]
    },

    "80_tasks_2_machines": {
        "coletiva": [
        "coletiva/coletiva_2048_80_2.out",
        "coletiva/coletiva_8192_80_2.out",
        "coletiva/coletiva_16384_80_2.out"
        ],
        "bloqueante": [
        "bloqueante/bloquante_2048_80_2.out",
        "bloqueante/bloquante_8192_80_2.out",
        "bloqueante/bloquante_16384_80_2.out"
        ],
        "nao_bloquante": [
        "naobloqueante/naobloqueante_2048_80_2.out",
        "naobloqueante/naobloqueante_8192_80_2.out",
        "naobloqueante/naobloqueante_16384_80_2.out"
        ]
    },

    "120_tasks_3_machines": {
        "coletiva": [
        "coletiva/coletiva_2048_120_3.out",
        "coletiva/coletiva_8192_120_3.out",
        "coletiva/coletiva_16384_120_3.out"
    ],
        "bloqueante": [
        "bloqueante/bloquante_2048_120_3.out",
        "bloqueante/bloquante_8192_120_3.out",
        "bloqueante/bloquante_16384_120_3.out"
    ],
        "nao_bloquante": [
        "naobloqueante/naobloqueante_2048_120_3.out",
        "naobloqueante/naobloqueante_8192_120_3.out",
        "naobloqueante/naobloqueante_16384_120_3.out"
    ] 
    },

    "160_tasks_4_machines": {
        "coletiva": [
        "coletiva/coletiva_2048_160_4.out",
        "coletiva/coletiva_8192_160_4.out",
        "coletiva/coletiva_16384_160_4.out"
    ],

        "bloquante": [
        "bloqueante/bloquante_2048_160_4.out",
        "bloqueante/bloquante_8192_160_4.out",
        "bloqueante/bloquante_16384_160_4.out"
    ],
        "nao_bloquante": [
        "naobloqueante/naobloqueante_2048_160_4.out",
        "naobloqueante/naobloqueante_8192_160_4.out", 
        "naobloqueante/naobloqueante_16384_160_4.out"
    ]
    }
}
def plot_grouped_lines(data, metric, title, ylabel):
    x_labels = list(data.keys())
    categories = list(next(iter(data.values())).keys())
    x_pos = np.arange(len(x_labels))

    plt.figure(figsize=(12, 6))

    for category in categories:
        values = [data[label][category] for label in x_labels]
        plt.plot(x_pos, values, marker='o', label=category)

    plt.xticks(x_pos, x_labels, rotation=45)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Tamanho do bloco da matriz")
    plt.legend(title="Categoria")
    plt.grid(axis='both', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

for group_name, categories in file_groups.items():
    # Inicializa o dicionário de métricas agrupadas
    metrics = {file.split('_')[1]: {} for file in next(iter(categories.values()))}

    for category, files in categories.items():
        for file in files:
            try:
                time_elapsed, cpus_utilized, insn_per_cycle = extract_values(file)
                size_key = file.split('_')[1]  # Extrai o tamanho da mensagem, ex.: '2048'
                
                #armazena as metricas para cada categorai e tamanho
                if size_key not in metrics:
                    metrics[size_key] = {}
                if category not in metrics[size_key]:
                    metrics[size_key][category] = {}

                metrics[size_key][category] = {
                    "time_elapsed": time_elapsed,
                    "cpus_utilized": cpus_utilized,
                    "insn_per_cycle": insn_per_cycle
                }
            except ValueError as e:
                print(e)

    # Plotar gráficos para cada métrica
    for metric, title, ylabel in [
        ("time_elapsed", "Tempo de Execução em Minutos", "Tempo (min)"),
        ("cpus_utilized", "Uso de CPUs", "CPU Utilizado (%)"),
        ("insn_per_cycle", "Instruções por Ciclo", "Inst/Ciclo"),
    ]:
        # Prepara os dados para a métrica específica
        metric_data = {
            size: {cat: data[cat][metric] for cat in data}
            for size, data in metrics.items()
        }

        # Plota o gráfico
        plot_grouped_lines(
            metric_data,
            metric,
            f"{title} ({group_name})",
            ylabel
        )