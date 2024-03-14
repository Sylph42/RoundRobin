from collections import deque
import numpy as np

class Processo:
    def __init__(self, nome, tempo_chegada, burst_time):
        self.nome = nome
        self.tempo_chegada = tempo_chegada
        self.burst_time = burst_time
        self.tempo_restante = burst_time
        self.tempo_espera = 0
        self.tempo_retorno = 0

def round_robin(processos, quantum):
    tempo_atual = 0
    fila_de_prontos = deque(processos)
    processo_atual = None
    sequencia_execucao = []

    while fila_de_prontos or processo_atual:
        if processo_atual is None and fila_de_prontos:
            processo_atual = fila_de_prontos.popleft()

        if processo_atual:
            sequencia_execucao.append(processo_atual.nome)
            tempo_execucao = min(quantum, processo_atual.tempo_restante)
            processo_atual.tempo_restante -= tempo_execucao
            tempo_atual += tempo_execucao

            if processo_atual.tempo_restante == 0:
                processo_atual.tempo_retorno = tempo_atual - processo_atual.tempo_chegada
                processo_atual = None
            else:
                fila_de_prontos.append(processo_atual)
                processo_atual = None
                tempo_atual += 1  # Tempo de mudança de contexto
        else:
            tempo_atual += 1

    return sequencia_execucao

def calcular_metricas(processos):
    tempos_espera = [p.tempo_espera for p in processos]
    tempos_retorno = [p.tempo_retorno for p in processos]

    tempo_medio_espera = np.mean(tempos_espera)
    tempo_medio_retorno = np.mean(tempos_retorno)
    vazao = len(processos) / max(p.tempo_retorno for p in processos)

    return tempo_medio_espera, tempo_medio_retorno, vazao

# Função para simulação
def simulacao(processos, quantums):
    for quantum in quantums:
        print(f"Simulação com Quantum = {quantum}")
        for p in processos:
            p.tempo_restante = p.burst_time
            p.tempo_espera = 0
            p.tempo_retorno = 0

        sequencia_execucao = round_robin(processos, quantum)
        print("Sequência de execução dos processos:", sequencia_execucao)

        tempo_medio_espera, tempo_medio_retorno, vazao = calcular_metricas(processos)

        print(f"Tempo médio de espera: {tempo_medio_espera}")
        print(f"Tempo médio de retorno: {tempo_medio_retorno}")
        print(f"Vazão: {vazao}\n")

# Exemplo de uso
processos = [
    Processo("P1", 0, 8),
    Processo("P2", 0, 4),
    Processo("P3", 0, 9),
    Processo("P4", 0, 5)
]

quantums = [1, 2, 3]

simulacao(processos, quantums)
