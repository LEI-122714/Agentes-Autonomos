import abc

class Ambiente(abc.ABC):
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.grid = [[None for _ in range(tamanho)] for _ in range(tamanho)]
        self.agentes = []

    @abc.abstractmethod
    def observacao_para(self, agente):
        pass

    @abc.abstractmethod
    def agir(self, acao, agente):
        pass

    @abc.abstractmethod
    def atualizacao(self):
        pass

    def get_posicao_valida(self, pos):
        x, y = pos
        x = max(0, min(x, self.tamanho - 1))
        y = max(0, min(y, self.tamanho - 1))
        return (x, y)