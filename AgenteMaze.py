import random
import numpy as np
from Agente import Agente

class AgenteMaze(Agente):
    def __init__(self, id_agente, posicao_inicial):
        super().__init__(id_agente, posicao_inicial)
        self.q_table = {}

        # Parâmetros de aprendizagem
        self.alpha = 0.1    # Taxa de aprendizagem
        self.gamma = 0.95   # Fator de desconto (aumentado para valorizar mais o futuro)
        self.epsilon = 1.0  # Começa com 100% exploração

        self.ultimo_estado = None
        self.ultima_acao = None
        self.percepcao_atual = None

    def get_q_values(self, estado):
        if estado not in self.q_table:
            # 4 ações possíveis (N, S, O, E)
            self.q_table[estado] = np.zeros(4)
        return self.q_table[estado]

    def estado_para_chave(self, obs):
        return obs["posicao"]

    def observacao(self, obs):
        self.percepcao_atual = obs

    def age(self):
        if self.percepcao_atual is None:
            return random.randint(0, 3)

        estado = self.estado_para_chave(self.percepcao_atual)
        self.ultimo_estado = estado

        # escolha da ação (epsilon-greedy)
        if self.learning_mode and random.uniform(0, 1) < self.epsilon:
            acao = random.randint(0, 3) # Exploração aleatória
        else:
            q_values = self.get_q_values(estado)
            max_val = np.max(q_values)
            # em caso de empate, escolhe aleatoriamente entre os melhores
            acoes_melhores = [i for i, v in enumerate(q_values) if v == max_val]
            acao = random.choice(acoes_melhores)

        self.ultima_acao = acao
        return acao

    def avaliacao_estado_atual(self, recompensa):
        # Atualiza a Q-Table com base na recompensa recebida (Q-Learning)
        if not self.learning_mode or self.ultimo_estado is None:
            return

        estado_antigo = self.ultimo_estado
        acao_antiga = self.ultima_acao

        estado_novo = self.estado_para_chave(self.percepcao_atual)

        q_antigo = self.get_q_values(estado_antigo)[acao_antiga]
        max_q_novo = np.max(self.get_q_values(estado_novo))

        # Fórmula Q-Learning
        novo_valor = q_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_antigo)
        self.q_table[estado_antigo][acao_antiga] = novo_valor