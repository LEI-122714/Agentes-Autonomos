import time
import os
import matplotlib.pyplot as plt  # <--- Biblioteca para o gráfico

from AmbienteFarol import AmbienteFarol
from AmbienteMaze import AmbienteMaze
from AgenteFarol import AgenteFarol
from AgenteMaze import AgenteMaze

class Simulador:
    def __init__(self):
        self.ambiente = None
        self.agentes = []
        self.passo_atual = 0
        self.max_passos = 0

    def _parse_posicao(self, linha):
        partes = linha.strip().split(',')
        if len(partes) < 2:
            partes = linha.strip().split(' ')
        return (int(partes[0]), int(partes[1]))

    def cria(self, ficheiro_parametros: str):
        print(f"A carregar configuração de: {ficheiro_parametros}")
        try:
            with open(ficheiro_parametros, 'r') as f:
                linhas = [l.strip() for l in f.readlines() if l.strip()]

            if not linhas: raise ValueError("Ficheiro vazio.")

            tipo_ambiente = linhas[0]

            if tipo_ambiente == "Farol":
                tamanho = int(linhas[1])
                pos_farol = self._parse_posicao(linhas[2])
                n_circulos = int(linhas[3])
                n_obstaculos_max = int(linhas[4])
                self.max_passos = int(linhas[5])

                self.ambiente = AmbienteFarol(tamanho, pos_farol, n_obstaculos_max, self.max_passos)
                self.agentes.append(AgenteFarol(1, (0, 0)))

            elif tipo_ambiente == "Maze":
                tamanho = int(linhas[1])
                pos_ini = self._parse_posicao(linhas[2])
                pos_final = self._parse_posicao(linhas[3])
                self.max_passos = int(linhas[5])

                self.ambiente = AmbienteMaze(tamanho, pos_ini, pos_final)
                self.agentes.append(AgenteMaze(1, pos_ini))

            else:
                raise ValueError("Tipo de ambiente desconhecido")

        except FileNotFoundError:
            print(f"Erro: O ficheiro '{ficheiro_parametros}' não foi encontrado.")
            raise
        except Exception as e:
            print(f"Erro ao ler ficheiro: {e}")
            raise
        return self

    def executa(self, visualizar=True):
        if visualizar:
            print(f" Início Simulação: {type(self.ambiente).__name__} ")

        terminou = False
        recompensa_total_episodio = 0

        while self.passo_atual < self.max_passos and not terminou:

            if visualizar and hasattr(self.ambiente, 'mostrar_estado'):
                self.ambiente.mostrar_estado(self.agentes)
                time.sleep(0.2)

            if hasattr(self.ambiente, 'atualizacao'):
                try: self.ambiente.atualizacao(self.agentes)
                except TypeError: self.ambiente.atualizacao()

            for agente in self.agentes:
                obs = self.ambiente.observacao_para(agente)
                agente.observacao(obs)

                acao = agente.age()
                recompensa = self.ambiente.agir(acao, agente)

                recompensa_total_episodio += recompensa

                nova_obs = self.ambiente.observacao_para(agente)
                agente.observacao(nova_obs)
                agente.avaliacao_estado_atual(recompensa)

                limite_sucesso = 50
                if isinstance(self.ambiente, AmbienteFarol):
                    limite_sucesso = 100

                if recompensa >= limite_sucesso:
                    terminou = True
                    if visualizar:
                        self.ambiente.mostrar_estado(self.agentes)
                        print(f"\n Sucesso! O agente terminou no passo {self.passo_atual}")

            self.passo_atual += 1

        if visualizar:
            if not terminou: print("\nTempo esgotado.")
            print("Simulação terminada.\n")

        return recompensa_total_episodio

if __name__ == "__main__":
    sim = Simulador()

    while True:
        try:
            ficheiro_input = input("Introduza o nome do ficheiro (ex: parametros-maze.txt ou parametros-farol.txt): ").strip()

            if os.path.exists(ficheiro_input):
                sim.cria(ficheiro_input)
                break
            else: print(f"Ficheiro não existe.\n")
        except Exception: print("Erro ao carregar ficheiro.")

    if not sim.agentes: exit()
    agente = sim.agentes[0]

    if isinstance(sim.ambiente, AmbienteMaze):
        print("\n Ambiente Maze ")
        NUM_EPISODIOS = 10000
        DECAY = 0.9997
    else:
        print("\n Ambiente Farol")
        NUM_EPISODIOS = 3000
        DECAY = 0.995

    print(f"A iniciar treino de {NUM_EPISODIOS} episódios.")
    start_time = time.time()

    agente.set_learning_mode(True)
    agente.epsilon = 1.0
    posicao_inicial = agente.posicao
    historico_recompensas = []

    for i in range(NUM_EPISODIOS):
        if hasattr(sim.ambiente, 'reset'): sim.ambiente.reset()

        agente.set_posicao(posicao_inicial)
        sim.passo_atual = 0

        recompensa_ep = sim.executa(visualizar=False)

        historico_recompensas.append(recompensa_ep)

        if agente.epsilon > 0.05: agente.epsilon *= DECAY

    print(f"Treino concluído.")

    def moving_average(a, n=100):
        ret = []
        import numpy as np
        if len(a) < n: return a
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    plt.figure(figsize=(10, 5))
    plt.plot(historico_recompensas, alpha=0.3, color='gray', label='Raw Data')

    if len(historico_recompensas) > 100:
        suavizado = moving_average(historico_recompensas)
        plt.plot(suavizado, color='blue', linewidth=2, label='Média Móvel (Tendência)')

    plt.title(f'Curva de Aprendizagem - {type(sim.ambiente).__name__}')
    plt.xlabel('Episódios')
    plt.ylabel('Recompensa Total')
    plt.legend()
    plt.grid(True)

    plt.show()

    time.sleep(1)

    print("\n Modo Teste ")
    if hasattr(sim.ambiente, 'reset'): sim.ambiente.reset()
    agente.set_learning_mode(False)
    agente.epsilon = 0
    agente.set_posicao(posicao_inicial)
    sim.passo_atual = 0
    sim.executa(visualizar=True)