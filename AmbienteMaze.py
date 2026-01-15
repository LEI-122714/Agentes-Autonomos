import random
from Ambiente import Ambiente

class AmbienteMaze(Ambiente):
    def __init__(self, tamanho, pos_inicial_agente, pos_saida):
        super().__init__(tamanho)
        self.pos_start = pos_inicial_agente
        self.pos_saida = pos_saida
        self.paredes = []

        self.gerar_labirinto()

    def gerar_labirinto(self):
        paredes_set = set()
        for x in range(self.tamanho):
            for y in range(self.tamanho):
                paredes_set.add((x, y))

        if self.pos_start in paredes_set:
            paredes_set.remove(self.pos_start)

        stack = [self.pos_start]

        while stack:
            cx, cy = stack[-1]
            vizinhos_possiveis = []
            deltas = [(0, -2, 0, -1), (0, 2, 0, 1), (-2, 0, -1, 0), (2, 0, 1, 0)]

            for dx, dy, wx, wy in deltas:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.tamanho and 0 <= ny < self.tamanho:
                    if (nx, ny) in paredes_set:
                        vizinhos_possiveis.append((nx, ny, wx, wy))

            if vizinhos_possiveis:
                nx, ny, wx, wy = random.choice(vizinhos_possiveis)
                paredes_set.remove((nx, ny))
                parede_intermedia = (cx + wx, cy + wy)
                if parede_intermedia in paredes_set:
                    paredes_set.remove(parede_intermedia)
                stack.append((nx, ny))
            else:
                stack.pop()

        if self.pos_saida in paredes_set:
            paredes_set.remove(self.pos_saida)

        fx, fy = self.pos_saida
        vizinhos = [(fx+1, fy), (fx-1, fy), (fx, fy+1), (fx, fy-1)]
        conectado = any((v not in paredes_set and 0 <= v[0] < self.tamanho and 0 <= v[1] < self.tamanho) for v in vizinhos)

        if not conectado:
            validos = [v for v in vizinhos if 0 <= v[0] < self.tamanho and 0 <= v[1] < self.tamanho]
            if validos:
                parede = random.choice(validos)
                if parede in paredes_set: paredes_set.remove(parede)

        self.paredes = list(paredes_set)

    def observacao_para(self, agente):
        x, y = agente.posicao
        vizinhos = {}
        direcoes = {'N':(0,-1), 'S':(0,1), 'O':(-1,0), 'E':(1,0)}

        for k, (dx, dy) in direcoes.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.tamanho and 0 <= ny < self.tamanho:
                if (nx, ny) in self.paredes: vizinhos[k] = 'Parede'
                else: vizinhos[k] = 'Livre'
            else:
                vizinhos[k] = 'Limite'

        return {
            "posicao": (x, y),
            "vizinhos": vizinhos,
            "saida": self.pos_saida
        }

    def agir(self, acao, agente):
        x, y = agente.posicao

        if acao == 0: y -= 1
        elif acao == 1: y += 1
        elif acao == 2: x -= 1
        elif acao == 3: x += 1

        nova_pos = self.get_posicao_valida((x, y))

        if nova_pos in self.paredes:
            return -5 # Penalidade por bater na parede

        agente.set_posicao(nova_pos)

        if nova_pos == self.pos_saida:
            return 100 # recompensa grande por encontrar a saída

        return -0.1 # penalidade pequena por passo

    def atualizacao(self, agentes=[]):
        pass

    def mostrar_estado(self, agentes):
        print(f"\n Labirinto ")
        mapa_visual = [['. ' for _ in range(self.tamanho)] for _ in range(self.tamanho)]

        for (px, py) in self.paredes: mapa_visual[py][px] = '# '

        sx, sy = self.pos_saida
        mapa_visual[sy][sx] = 'S '

        for agente in agentes:
            ax, ay = agente.posicao
            char = 'A '
            if (ax, ay) == (sx, sy): char = 'A*'
            mapa_visual[ay][ax] = char

        for linha in mapa_visual: print("".join(linha))