import random
import numpy as np
from Agente import Agente

class AgenteFarol(Agente):
    def __init__(self, id_agente, posicao_inicial):
        super().__init__(id_agente, posicao_inicial)
        self.q_table = {}

        self.alpha = 0.1   # taxa de aprendizagem
        self.gamma = 0.9   # fator de desconto
        self.epsilon = 0.1 # taxa de exploração

        self.ultimo_estado = None
        self.ultima_acao = None
        self.percepcao_atual = None

    def get_q_values(self, estado):
        if estado not in self.q_table:
            self.q_table[estado] = np.zeros(4) # 4 ações
        return self.q_table[estado]

    def estado_para_chave(self, obs):

        dx, dy = obs["direcao_farol"]
        sensores = obs["sensores"]

        s_dx = 0 # 0 = alinhado
        if dx > 0: s_dx = 1 # 1 = direita
        elif dx < 0: s_dx = -1 # -1 = esquerda

        s_dy = 0
        if dy > 0: s_dy = 1 # 1 = baixo
        elif dy < 0: s_dy = -1 # -1 = cima

        return (s_dx, s_dy, sensores)

    def observacao(self, obs):
        self.percepcao_atual = obs

    def age(self):

        if self.percepcao_atual is None:
            return random.randint(0, 3)

        estado = self.estado_para_chave(self.percepcao_atual)
        self.ultimo_estado = estado

        if self.learning_mode and random.uniform(0, 1) < self.epsilon:
            acao = random.randint(0, 3)
        else:
            q_values = self.get_q_values(estado)
            max_val = np.max(q_values)
            acoes_melhores = [i for i, v in enumerate(q_values) if v == max_val]
            acao = random.choice(acoes_melhores)

        self.ultima_acao = acao
        return acao

    def avaliacao_estado_atual(self, recompensa):

        if not self.learning_mode or self.ultimo_estado is None:
            return

        estado_antigo = self.ultimo_estado
        acao_antiga = self.ultima_acao

        estado_novo = self.estado_para_chave(self.percepcao_atual)

        q_antigo = self.get_q_values(estado_antigo)[acao_antiga]
        max_q_novo = np.max(self.get_q_values(estado_novo))

        # Q-Learning
        novo_valor = q_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_antigo)
        self.q_table[estado_antigo][acao_antiga] = novo_valor