import math
import random
from Ambiente import Ambiente

class AmbienteFarol(Ambiente):
    def __init__(self, tamanho, pos_farol, n_obstaculos_max, max_steps):
        super().__init__(tamanho)
        self.pos_farol = pos_farol
        self.n_obstaculos_max = n_obstaculos_max
        self.max_steps = max_steps
        self.obstaculos = []
        self.current_step = 0

        self.reset()

    def reset(self):
        self.current_step = 0
        self.obstaculos = []
        self.gerar_obstaculos_estaticos()

    def gerar_obstaculos_estaticos(self):
        tentativas = 0
        max_tentativas = self.tamanho * self.tamanho * 2

        while len(self.obstaculos) < self.n_obstaculos_max and tentativas < max_tentativas:
            tentativas += 1
            ox = random.randint(0, self.tamanho-1)
            oy = random.randint(0, self.tamanho-1)

            posicoes_proibidas = [self.pos_farol, (0, 0)]

            if (ox, oy) not in posicoes_proibidas and (ox, oy) not in self.obstaculos:
                self.obstaculos.append((ox, oy))

    def observacao_para(self, agente):
        ax, ay = agente.posicao
        fx, fy = self.pos_farol

        dx = fx - ax
        dy = fy - ay
        distancia = math.sqrt(dx**2 + dy**2)

        sensores = []
        direcoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for move_x, move_y in direcoes:
            nx, ny = ax + move_x, ay + move_y

            bloqueado = 0
            if not (0 <= nx < self.tamanho and 0 <= ny < self.tamanho):
                bloqueado = 1
            elif (nx, ny) in self.obstaculos:
                bloqueado = 1

            sensores.append(bloqueado)

        return {
            "direcao_farol": (dx, dy),
            "distancia": distancia,
            "posicao_agente": (ax, ay),
            "sensores": tuple(sensores)
        }

    def agir(self, acao, agente):
        x, y = agente.posicao

        if acao == 0: y -= 1
        elif acao == 1: y += 1
        elif acao == 2: x -= 1
        elif acao == 3: x += 1

        nova_pos = self.get_posicao_valida((x, y))

        if nova_pos in self.obstaculos:
            return -10 # penalidade por colisão

        agente.set_posicao(nova_pos)

        dist = math.sqrt((self.pos_farol[0] - nova_pos[0])**2 + (self.pos_farol[1] - nova_pos[1])**2)

        if dist == 0:
            return 100 # recompensa máxima

        return -1 # penalidade de tempo

    def atualizacao(self, agentes=[]):
        self.current_step += 1

    def mostrar_estado(self, agentes):
        print(f"\nPasso {self.current_step} ")
        mapa_visual = [['. ' for _ in range(self.tamanho)] for _ in range(self.tamanho)]

        for (ox, oy) in self.obstaculos:
            mapa_visual[oy][ox] = '# '

        fx, fy = self.pos_farol
        if 0 <= fx < self.tamanho and 0 <= fy < self.tamanho:
            mapa_visual[fy][fx] = 'F '

        for agente in agentes:
            ax, ay = agente.posicao
            if 0 <= ax < self.tamanho and 0 <= ay < self.tamanho:
                char = 'A '
                if (ax, ay) == (fx, fy): char = 'A*'
                mapa_visual[ay][ax] = char

        for linha in mapa_visual:
            print("".join(linha))
