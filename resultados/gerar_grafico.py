
import csv
import matplotlib.pyplot as plt

geracoes = []
melhores = []
medias = []
piores = []


with open("historico.csv", "r", newline="", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        geracoes.append(int(linha["geracao"]))
        melhores.append(float(linha["melhor"]))
        medias.append(float(linha["media"]))
        piores.append(float(linha["pior"]))

plt.figure(figsize=(10, 6))

plt.plot(geracoes, melhores, marker="o", label="Melhor fitness")
plt.plot(geracoes, medias, marker="o", label="Fitness médio")
plt.plot(geracoes, piores, marker="o", label="Pior fitness")

plt.title("Evolução do Algoritmo Genético - Freeway")
plt.xlabel("Geração")
plt.ylabel("Fitness (recompensa acumulada)")

plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()


plt.savefig("grafico_evolucao.png", dpi=300)


plt.show()

print("Gráfico salvo em grafico_evolucao.png")