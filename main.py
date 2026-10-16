
import copy
import csv
import os

import ale_py
import gymnasium as gym
import numpy as np

gym.register_envs(ale_py)

# Configurações do ambiente e do algoritmo genético
ENV_ID = "ALE/Breakout-v5"

TAMANHO_POPULACAO = 10
NUM_GERACOES = 10

NUM_ENTRADAS = 128
NUM_OCULTOS = 16
NUM_ACOES = 4

TAXA_MUTACAO = 0.10
INTENSIDADE_MUTACAO = 0.20
NUM_ELITE = 2


def criar_ambiente(render_mode=None):
    """Cria o ambiente Atari Breakout usando a memória RAM."""
    return gym.make(
        ENV_ID,
        obs_type="ram",
        render_mode=render_mode
    )


class Agente:
    """Rede neural simples utilizada pelo agente."""

    def __init__(self):
        self.W1 = np.random.randn(NUM_ENTRADAS, NUM_OCULTOS)
        self.b1 = np.random.randn(NUM_OCULTOS)

        self.W2 = np.random.randn(NUM_OCULTOS, NUM_ACOES)
        self.b2 = np.random.randn(NUM_ACOES)

        self.fitness = 0.0

    def agir(self, estado):
        """Escolhe uma ação com base no estado atual."""
        estado = estado.astype(np.float32) / 255.0

        oculto = np.tanh(estado @ self.W1 + self.b1)
        saida = oculto @ self.W2 + self.b2

        return int(np.argmax(saida))


def avaliar(agente):
    """Executa uma partida e retorna a recompensa acumulada."""
    env = criar_ambiente()

    estado, info = env.reset()

    fitness = 0.0
    terminado = False
    truncado = False

    precisa_disparar = True
    vidas_anteriores = info.get("lives")

    while not terminado and not truncado:
        if precisa_disparar:
            # Ação FIRE para iniciar a partida ou continuar após perder uma vida.
            acao = 1
            precisa_disparar = False
        else:
            acao = agente.agir(estado)

        novo_estado, recompensa, terminado, truncado, info = env.step(acao)

        fitness += recompensa

        vidas_atuais = info.get("lives", vidas_anteriores)

        if (
            vidas_anteriores is not None
            and vidas_atuais < vidas_anteriores
        ):
            precisa_disparar = True

        vidas_anteriores = vidas_atuais
        estado = novo_estado

    env.close()

    return fitness


def criar_populacao():
    """Cria a população inicial de agentes."""
    return [
        Agente()
        for _ in range(TAMANHO_POPULACAO)
    ]


def selecionar(populacao):
    """Seleciona os 50% de agentes com maior fitness."""
    populacao_ordenada = sorted(
        populacao,
        key=lambda agente: agente.fitness,
        reverse=True
    )

    quantidade_pais = TAMANHO_POPULACAO // 2

    return populacao_ordenada[:quantidade_pais]


def mutar(agente):
    """Aplica mutações aleatórias aos parâmetros da rede neural."""
    for nome in ("W1", "b1", "W2", "b2"):
        parametros = getattr(agente, nome)

        mascara = (
            np.random.rand(*parametros.shape) < TAXA_MUTACAO
        )

        ruido = (
            np.random.randn(*parametros.shape)
            * INTENSIDADE_MUTACAO
        )

        parametros += mascara * ruido


def nova_geracao(populacao):
    """Gera uma nova população usando seleção, elitismo e mutação."""
    pais = selecionar(populacao)

    pais = sorted(
        pais,
        key=lambda agente: agente.fitness,
        reverse=True
    )

    nova_populacao = []

    # Preserva os melhores agentes sem alterações.
    for i in range(NUM_ELITE):
        elite = copy.deepcopy(pais[i])
        nova_populacao.append(elite)

    # Cria os demais agentes a partir dos pais selecionados.
    while len(nova_populacao) < TAMANHO_POPULACAO:
        indice_pai = np.random.randint(len(pais))
        pai = pais[indice_pai]

        filho = copy.deepcopy(pai)
        filho.fitness = 0.0

        mutar(filho)

        nova_populacao.append(filho)

    return nova_populacao


def salvar_historico(historico):
    """Salva os resultados na pasta resultados."""
    pasta_resultados = "resultados"

    # Cria a pasta caso ela não exista.
    os.makedirs(pasta_resultados, exist_ok=True)

    caminho_csv = os.path.join(
        pasta_resultados,
        "historico.csv"
    )

    with open(
        caminho_csv,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        campos = [
            "geracao",
            "melhor",
            "media",
            "pior"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(historico)

    print(f"Histórico salvo em {caminho_csv}")


def main():
    """Executa o algoritmo genético."""
    populacao = criar_populacao()
    historico = []

    for geracao in range(NUM_GERACOES):
        # Avalia todos os agentes da geração atual.
        for agente in populacao:
            agente.fitness = avaliar(agente)

        valores = [
            agente.fitness
            for agente in populacao
        ]

        melhor = max(valores)
        media = float(np.mean(valores))
        pior = min(valores)

        historico.append({
            "geracao": geracao,
            "melhor": melhor,
            "media": media,
            "pior": pior
        })

        print(
            f"Geração {geracao:03d} | "
            f"Melhor: {melhor:.2f} | "
            f"Média: {media:.2f} | "
            f"Pior: {pior:.2f}"
        )

        # Cria a população da próxima geração.
        populacao = nova_geracao(populacao)

    salvar_historico(historico)


if __name__ == "__main__":
    main()