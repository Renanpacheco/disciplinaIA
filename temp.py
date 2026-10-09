import pandas as pd

df = pd.DataFrame(historico)

df.to_csv("historico_freeway.csv", index=False)

print("CSV salvo!")

import matplotlib.pyplot as plt

geracoes = [x["geracao"] for x in historico]
melhor = [x["melhor"] for x in historico]
media = [x["media"] for x in historico]

plt.plot(geracoes, melhor, label="Melhor")
plt.plot(geracoes, media, label="Média")

plt.xlabel("Geração")
plt.ylabel("Fitness")
plt.title("Evolução da População")

plt.legend()

plt.show()
melhor_agente = max(populacao, key=lambda a: a.fitness)

env = criar_ambiente(render_mode="human")

estado, info = env.reset()

terminado = False
truncado = False

while not (terminado or truncado):

    acao = melhor_agente.agir(estado)

    estado, recompensa, terminado, truncado, info = env.step(acao)

env.close()