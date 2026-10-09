# Algoritmo Genético aplicado ao Atari Freeway

## 1. Objetivo

Este projeto utiliza um algoritmo genético para otimizar os parâmetros de uma rede neural que controla um agente no jogo Atari Freeway. O objetivo é investigar como a seleção, o elitismo e a mutação influenciam o desempenho dos agentes ao longo das gerações.

Cada indivíduo da população representa uma rede neural com parâmetros próprios. O desempenho é medido pelo fitness, calculado a partir da soma das recompensas obtidas durante um episódio.

## 2. Tecnologias utilizadas

* Python 3
* NumPy
* Gymnasium
* ALE-Py
* Matplotlib
* CSV, para armazenamento dos resultados

## 3. Ambiente e observações

* **Ambiente:** `ALE/Freeway-v5`
* **Biblioteca:** Gymnasium com ALE-Py
* **Tipo de observação:** RAM (`obs_type="ram"`)
* **Entradas da rede neural:** 128 valores da RAM do Atari
* **Camada oculta:** 16 neurônios
* **Saídas:** 3 valores correspondentes às ações disponíveis
* **Função de ativação:** tangente hiperbólica (`tanh`)
* **Critério de escolha da ação:** maior valor de saída (`argmax`)
* **Fitness:** soma das recompensas acumuladas durante o episódio

A observação por RAM utiliza os dados internos do ambiente, em vez de fornecer imagens do jogo à rede neural. Os valores são convertidos para ponto flutuante e normalizados pela divisão por 255.

## 4. Configuração do experimento

| Parâmetro                             |                               Valor |
| ------------------------------------- | ----------------------------------: |
| Ambiente                              |                    `ALE/Freeway-v5` |
| Tamanho da população                  |                       20 indivíduos |
| Número de gerações                    |                                  30 |
| Entradas da rede neural               |                                 128 |
| Neurônios ocultos                     |                                  16 |
| Saídas da rede neural                 |                                   3 |
| Estratégia de seleção                 | Seleção dos 50% melhores indivíduos |
| Quantidade de indivíduos selecionados |                                  10 |
| Elitismo                              |                        2 indivíduos |
| Taxa de mutação                       |                          0,10 (10%) |
| Intensidade da mutação                |                                0,20 |

### Seleção

Os indivíduos são ordenados de acordo com o fitness em ordem decrescente. Os 10 melhores são selecionados para participar da reprodução.

### Elitismo

Os dois melhores indivíduos entre os selecionados são copiados para a geração seguinte sem alterações. Essa estratégia preserva soluções de alto desempenho.

### Mutação

Cada parâmetro da rede neural possui 10% de probabilidade de sofrer uma alteração aleatória. A perturbação é obtida por uma distribuição normal, multiplicada pela intensidade de mutação de 0,20.

Os descendentes são criados a partir de cópias dos pais e recebem mutações. Nesta implementação, não é utilizado cruzamento (crossover) entre dois indivíduos.

## 5. Instalação e execução

### Pré-requisitos

É necessário ter Python 3 e pip instalados.

### Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone <URL_DO_REPOSITORIO>
cd <projeto2>
```

Crie e ative um ambiente virtual.

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install numpy gymnasium ale-py matplotlib
```

### Executar o experimento

Execute o script principal:

```bash
python main.py
```

Ao finalizar o treinamento, o programa deverá gerar o arquivo `historico.csv`, contendo o melhor, o médio e o pior fitness de cada geração.

Para gerar o gráfico de evolução:

```bash
cd resultados
python gerar_grafico.py
```

O script de visualização deverá ler `historico.csv` e salvar `grafico_evolucao.png`.

## 6. Resultados experimentais

Foram previstos três experimentos para analisar o comportamento do algoritmo genético. Os resultados devem ser registrados individualmente, utilizando os arquivos CSV produzidos por cada execução.

### Experimento 1

**Configuração:** população de 20 indivíduos, 30 gerações, elitismo de 2 indivíduos e mutação de 10%, com intensidade de 0,20.

Resultados observados:

* Melhor fitness: 28, na geração 21.
* Melhor fitness na última geração: 27.
* Maior fitness médio: 24,10, na geração 28.
* Fitness médio na última geração: 22,70.
* Pior fitness na última geração: 12.

## 7. Gráfico de evolução

O gráfico de evolução deve apresentar duas curvas principais:

* **Melhor fitness por geração:** permite acompanhar o melhor desempenho obtido em cada geração.
* **Fitness médio por geração:** permite observar a evolução geral da população.

O gráfico gerado a partir dos dados do primeiro experimento deverá ser salvo em `grafico_evolucao.png` e incluído neste README.

Após adicionar a imagem ao repositório, utilize:

```markdown
![Evolução do melhor e do fitness médio](grafico_evolucao.png)
```

A comparação entre os três experimentos deve utilizar os respectivos históricos, permitindo verificar o efeito das configurações sobre o desempenho e a convergência.

## 8. Análise de exploração e convergência

No primeiro experimento, houve uma melhora expressiva nas primeiras gerações. O fitness médio aumentou de 3,40 na geração 0 para 22,25 na geração 3. Esse comportamento indica que a seleção e a reprodução permitiram encontrar rapidamente redes neurais com desempenho superior ao das soluções iniciais.

Após a geração 10, o melhor fitness passou a oscilar predominantemente entre 26 e 27, atingindo 28 na geração 21. O fitness médio também apresentou oscilações, com seu maior valor na geração 28. Esses resultados sugerem uma fase de ganhos marginais e possível estagnação parcial.

A mutação permite explorar novas configurações dos pesos e vieses da rede neural. Entretanto, alterações aleatórias também podem prejudicar indivíduos que anteriormente apresentavam bom desempenho. Na geração 29, o pior fitness caiu de 21 para 12, enquanto a média caiu de 24,10 para 22,70.

A queda pode estar relacionada à deterioração de descendentes após a mutação ou à variabilidade na avaliação dos episódios. Os dados agregados, isoladamente, não permitem determinar a causa.

O elitismo preserva dois indivíduos sem mutação, reduzindo o risco de perder as melhores soluções encontradas nas gerações anteriores. Entretanto, ele não impede a redução do desempenho médio ou do pior fitness.

Para avaliar melhor a exploração e a convergência, recomenda-se comparar diferentes taxas e intensidades de mutação, executar múltiplas repetições com sementes controladas e avaliar os agentes em mais de um episódio.

## 9. Conclusão

O primeiro experimento demonstrou uma melhora rápida do desempenho inicial, seguida por uma fase de evolução mais lenta. O melhor fitness alcançado foi 28, mas o desempenho não apresentou crescimento consistente nas últimas gerações.

Os próximos experimentos devem investigar se mudanças na taxa de mutação, na intensidade das alterações e no tamanho da população podem melhorar o desempenho médio e a estabilidade das soluções.

A comparação dos três experimentos permitirá analisar de maneira mais consistente o equilíbrio entre exploração de novas soluções, preservação dos melhores indivíduos e convergência do algoritmo genético.
