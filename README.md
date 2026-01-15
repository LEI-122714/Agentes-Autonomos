# Agentes Autónomos: Simulador de Sistemas Multi-Agente

O projeto encontra-se no branch Master. Não estava a ser possível merge com o main. 

## Como testar o projeto

Para testar o projeto, basta correr o ficheiro Simulador.py e escrever o nome do ficheiro de parâmetros que se pretende utilizar para a simulação na consola seguido da mensagem “Introduza o nome do ficheiro: ”.

Existem ja dois ficheiros existentes próprios para testar cada ambiente do projeto denominados de "parametros-farol.txt" e "parametros-maze.txt".

É possível adicionar um novo ficheiro .txt ao projeto e utilizá-lo para testar, desde que siga as regras.

### Configuração do ficheiro:

O ficheiro de parâmetros, se for do ambiente farol, deve seguir a seguinte configuração:

1. Farol (Tipo de Ambiente)
2. n (tamanho lateral da grelha)
3. x,y (posição do farol)
4. n (“luz do farol” o farol erradia 3 camadas de luz à sua volta que o agente consegue ver para se guiar até ele)
5. n (número de obstáculos)
6. n (número máximo de passos “timer”)

Se for do ambiente maze, deve seguir a seguinte configuração:

1. Maze (Tipo de Ambiente)
2. n (tamanho lateral da grelha)
3. x,y (posição inicial do agente)
4. x,y (posição da saída)
5. n (número máximo de obstáculos)
6. n (número máximo de passos “timer”)
