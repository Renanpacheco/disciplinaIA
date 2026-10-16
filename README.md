# Algoritmo Genético aplicado ao Atari Breakout

## 1. Descrição do projeto

Este projeto utiliza um **algoritmo genético** para otimizar uma rede neural simples capaz de tomar decisões no jogo Atari Breakout. O objetivo é evoluir agentes por meio de seleção, elitismo e mutação, buscando aumentar a recompensa obtida durante as partidas.

O ambiente é executado por meio da biblioteca Gymnasium, utilizando o ALE (Arcade Learning Environment).

## 2. Tecnologias utilizadas

* Python
* NumPy
* Gymnasium
* ALE-Py
* Matplotlib

## 3. Estrutura do projeto

```text
disciplinaIA/
├── main.py
└── resultados/
    ├── gerar_grafico.py
    ├── historico.csv
    └── grafico_evolucao.png
```

* `main.py`: executa o algoritmo genético e salva os resultados de cada geração.
* `resultados/gerar_grafico.py`: lê os dados do CSV e gera o gráfico de evolução.
* `resultados/historico.csv`: armazena o melhor, o pior e o fitness médio de cada geração.
* `resultados/grafico_evolucao.png`: imagem gerada pelo script de visualização.

Os arquivos `historico.csv` e `grafico_evolucao.png` são gerados durante a execução dos respectivos scripts.

## 4. Configuração do experimento

O experimento foi executado com os seguintes parâmetros:

| Parâmetro                           |             Valor |
| ----------------------------------- | ----------------: |
| Ambiente                            | `ALE/Breakout-v5` |
| Tipo de observação                  |       Memória RAM |
| Entradas da rede neural             |               128 |
| Neurônios na camada oculta          |                16 |
| Saídas da rede neural               |                 4 |
| Tamanho da população                |                10 |
| Número de gerações                  |                10 |
| Pais selecionados por geração       |                 5 |
| Indivíduos preservados por elitismo |                 2 |
| Taxa de mutação                     |              0,10 |
| Intensidade da mutação              |              0,20 |

### Rede neural

A rede neural recebe os 128 valores da memória RAM do ambiente, normalizados para o intervalo de 0 a 1. Esses valores são processados por uma camada oculta de 16 neurônios, que utiliza a função de ativação tangente hiperbólica (`tanh`).

A camada de saída possui quatro valores, correspondentes às ações disponíveis para o agente. A ação escolhida é aquela que apresenta o maior valor de saída (`argmax`).

### Fitness

O fitness representa a soma das recompensas obtidas pelo agente durante uma partida. No Breakout, a recompensa está relacionada ao desempenho no jogo, como atingir os tijolos.

Quanto maior o fitness, melhor foi o desempenho do agente naquela avaliação.

## 5. Funcionamento do algoritmo genético

O algoritmo segue estas etapas:

1. **Inicialização:** criação de uma população com 10 agentes, cada um com parâmetros aleatórios na rede neural.
2. **Avaliação:** execução de uma partida para cada agente, registrando sua recompensa acumulada como fitness.
3. **Seleção:** escolha dos cinco agentes com maior fitness para compor o grupo de pais.
4. **Elitismo:** preservação dos dois melhores agentes, sem alterações em seus parâmetros.
5. **Reprodução:** criação de novos indivíduos a partir de cópias dos pais selecionados.
6. **Mutação:** alteração aleatória de parte dos pesos e vieses da rede neural.
7. **Nova geração:** formação de uma população de 10 agentes, que será avaliada novamente.

O processo é repetido até completar as 10 gerações configuradas.

## 6. Como executar o projeto

### Pré-requisitos

* Python instalado.
* Git instalado, caso o projeto seja clonado do GitHub.

### Clonar o repositório

```bash
git clone https://github.com/Renanpacheco/disciplinaIA.git
cd disciplinaIA
```

### Criar e ativar o ambiente virtual

No Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar as dependências

O projeto utiliza o arquivo `requirements.txt` para instalar as bibliotecas e suas versões registradas.

```bash
pip install -r requirements.txt
```

### Executar o algoritmo genético

Na raiz do projeto, execute:

```bash
python main.py
```

O programa executará o algoritmo genético e salvará os resultados das gerações no arquivo:

```text
resultados/historico.csv
```

### Gerar o gráfico dos resultados

Depois que a execução do algoritmo terminar, gere o gráfico com:

```bash
python resultados/gerar_grafico.py
```

O gráfico será salvo em:

```text
resultados/grafico_evolucao.png
```


## 7. Resultados do experimento

Os resultados obtidos nas 10 gerações foram:

| Geração | Melhor fitness | Fitness médio | Pior fitness |
| ------: | -------------: | ------------: | -----------: |
|       0 |            7,0 |           3,8 |          0,0 |
|       1 |           11,0 |           5,6 |          1,0 |
|       2 |           11,0 |           3,9 |          1,0 |
|       3 |           11,0 |           8,2 |          3,0 |
|       4 |           11,0 |           6,9 |          2,0 |
|       5 |           11,0 |           5,5 |          0,0 |
|       6 |           11,0 |           8,5 |          2,0 |
|       7 |           11,0 |           5,1 |          2,0 |
|       8 |           11,0 |           5,8 |          1,0 |
|       9 |           11,0 |           5,8 |          3,0 |

### Análise dos resultados

O melhor fitness aumentou de 7,0 na geração inicial para 11,0 na primeira geração seguinte. Esse valor permaneceu constante até a geração 9.

A permanência do melhor resultado pode indicar estagnação da evolução, mas não é suficiente para concluir que o algoritmo atingiu uma solução ótima.