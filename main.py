import copy
import gymnasium as gym
import ale_py
import numpy as np
gym.register_envs(ale_py)
import csv
# ---------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------
ENV_ID = "ALE/Freeway-v5"
TAMANHO_POPULACAO = 20
NUM_GERACOES = 30
NUM_ENTRADAS = 128
NUM_OCULTOS = 16
NUM_ACOES = 3
TAXA_MUTACAO = 0.10
INTENSIDADE_MUTACAO = 0.20
NUM_ELITE = 2

def criar_ambiente(render_mode=None):
    return gym.make(
        ENV_ID,
        obs_type="ram",
        render_mode=render_mode
    )

class Agente:
    def __init__(self):
# Cada indivíduo começa com parâmetros diferentes.
        self.W1 = np.random.randn(NUM_ENTRADAS, NUM_OCULTOS)
        self.b1 = np.random.randn(NUM_OCULTOS)
        self.W2 = np.random.randn(NUM_OCULTOS, NUM_ACOES)
        self.b2 = np.random.randn(NUM_ACOES)
        self.fitness = 0.0

    def agir(self, estado):
# RAM: valores inteiros entre 0 e 255.
        estado = estado.astype(np.float32) / 255.0
        oculto = np.tanh(estado @ self.W1 + self.b1)
        saida = oculto @ self.W2 + self.b2
# A maior saída define a ação escolhida.
        return int(np.argmax(saida))


def avaliar(agente):

    env = criar_ambiente()

    estado, info = env.reset()

    fitness = 0.0
    terminado = False
    truncado = False
    

    while not terminado and not truncado:
        
        acao = agente.agir(estado)
        
        novo_estado, recompensa, terminado, truncado, info = env.step(acao)
        

        
        fitness += recompensa

        
        estado = novo_estado

    env.close()
    

    return fitness

def criar_populacao():
    
    pop=[]
    for i in range(TAMANHO_POPULACAO):
        pop.append(Agente())
    
        
    return(pop)


def selecionar(populacao):
    

    populacao_ordenada = sorted(
        populacao,
        key=lambda agente: agente.fitness,
        reverse=True
    )
    

    quantidade_pais = TAMANHO_POPULACAO // 2

    return populacao_ordenada[:quantidade_pais]


def mutar(agente):

    
    mascara = np.random.rand(*agente.W1.shape) < TAXA_MUTACAO
    agente.W1 += mascara * (
        np.random.randn(*agente.W1.shape) * INTENSIDADE_MUTACAO
    )

    
    mascara = np.random.rand(*agente.b1.shape) < TAXA_MUTACAO
    agente.b1 += mascara * (
        np.random.randn(*agente.b1.shape) * INTENSIDADE_MUTACAO
    )

    
    mascara = np.random.rand(*agente.W2.shape) < TAXA_MUTACAO
    agente.W2 += mascara * (
        np.random.randn(*agente.W2.shape) * INTENSIDADE_MUTACAO
    )

    
    mascara = np.random.rand(*agente.b2.shape) < TAXA_MUTACAO
    agente.b2 += mascara * (
        np.random.randn(*agente.b2.shape) * INTENSIDADE_MUTACAO
    )


def nova_geracao(populacao):
    
    pais = selecionar(populacao)

    pais = sorted(
        pais,
        key=lambda agente: agente.fitness,
        reverse=True
    )

    nova_populacao = []

    for i in range(NUM_ELITE):
        elite = copy.deepcopy(pais[i])
        nova_populacao.append(elite)

    while len(nova_populacao) < TAMANHO_POPULACAO:

        
        pai = np.random.choice(pais)

        
        filho = copy.deepcopy(pai)

        
        filho.fitness = 0.0

        
        mutar(filho)

        nova_populacao.append(filho)

    return nova_populacao
populacao = criar_populacao()
historico = []
for geracao in range(NUM_GERACOES):
# Avaliar TODOS os indivíduos da geração.
    for agente in populacao:
        agente.fitness = avaliar(agente)
    valores = [agente.fitness for agente in populacao]
    melhor = max(valores)
    media = float(np.mean(valores))
    pior = min(valores)
    historico.append({
        "geracao": geracao,
        "melhor": melhor,
        "media": media,
        "pior": pior,
    })
    
    print(
        f"Geração {geracao:03d} | "
        f"Melhor: {melhor:.2f} | "
        f"Média: {media:.2f} | "
        f"Pior: {pior:.2f}"
    )
    # Produzir a próxima geração.
    populacao = nova_geracao(populacao)
    
    
with open("historico.csv", "w", newline="", encoding="utf-8") as arquivo:
    campos = ["geracao", "melhor", "media", "pior"]

    escritor = csv.DictWriter(arquivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(historico)

print("Histórico salvo em historico.csv")
