import abc

class Agente(abc.ABC):
    def __init__(self, id_agente, posicao_inicial=None):
        self.id = id_agente
        self.posicao = posicao_inicial
        self.recompensa_acumulada = 0
        self.learning_mode = True

    @abc.abstractmethod
    def observacao(self, obs):
        pass

    @abc.abstractmethod
    def age(self):
        pass

    @abc.abstractmethod
    def avaliacao_estado_atual(self, recompensa):
        pass

    def set_learning_mode(self, mode: bool):
        self.learning_mode = mode

    def set_posicao(self, pos):
        self.posicao = pos