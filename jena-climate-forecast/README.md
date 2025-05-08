
# 🌡️ Previsão de Temperatura com Séries Temporais — Projeto com Dataset Jena Climate

Este projeto realiza a previsão da temperatura nas próximas 24 horas com base em dados meteorológicos históricos do dataset **Jena Climate**. Utilizamos diferentes modelos, com foco no **LSTM**, **AutoARIMA**, **Prophet** e outros métodos estatísticos e de aprendizado de máquina. A métrica de avaliação principal é o **erro absoluto médio (MAE)**.

---

## 🚀 Como Usar o Projeto

### 📁 Estrutura do Projeto

- `src/`: scripts Python modularizados para modelagem e avaliação
- `notebooks/`: notebooks de análise exploratória e visualizações
- `data/`: dataset original (Jena Climate)
- `main.py`: pipeline completo de pré-processamento, modelagem e previsão
- `requirements.txt`: dependências do projeto

### ▶️ Executando Localmente

```bash
git clone https://github.com/seu-usuario/jena-climate-forecast.git
cd jena-climate-forecast
pip install -r requirements.txt
python main.py
```

> Certifique-se de ter Python 3.8+ instalado.

---

## 📘 Estudo Técnico: Previsão de Temperatura com Modelos Temporais

### 1. Introdução

A previsão de temperatura é uma tarefa central em aplicações meteorológicas e setores sensíveis ao clima. Este projeto propõe a construção de um modelo preditivo para estimar a temperatura nas próximas 24 horas, com base em dados históricos. A acurácia do modelo é avaliada pela métrica **MAE**.

---

### 2. Metodologia

Diversos modelos foram avaliados com o objetivo de comparar precisão, robustez e interpretabilidade:

- **Modelos Lineares**: Regressão Linear
- **Séries Temporais**: ARIMA, ARIMAX
- **Redes Neurais**: ANN, RNN, LSTM
- **Modelos com Árvores de Decisão**
- **Prophet (Facebook)**

Cada abordagem explora diferentes formas de capturar padrões sazonais, tendência e variabilidade dos dados climáticos.

---

### 3. Análise Exploratória dos Dados (EDA)

#### 3.1 Dados Faltantes e Outliers

Valores como `-9999.0` foram identificados em variáveis como `wv` e `max. wv`, e substituídos por interpolação linear. Valores extremos foram suavizados.

📈 **Gráfico 1 — Série Temporal da Temperatura**  
![Gráfico 1](https://github.com/user-attachments/assets/41e29da2-364c-4b35-b897-7b83b049c95d)

#### 3.2 Estatísticas Descritivas

O conjunto de dados apresenta temperatura média de 9,44 °C, com ampla variação entre –22,65 °C e 37,04 °C. Variáveis como pressão, densidade do ar e temperatura potencial seguem distribuições aproximadamente normais, tornando-se adequadas para modelos lineares. Em contraste, variáveis como concentração de vapor e velocidade do vento exibem distribuições assimétricas à direita, podendo exigir transformações logarítmicas. A direção do vento apresenta distribuição bimodal, e a umidade relativa concentra-se entre 60% e 100%, com cauda inferior mais longa.


📊 **Gráfico 2 — Distribuições das Variáveis**  
![Gráfico 2](https://github.com/user-attachments/assets/70d58186-e2f2-43bc-bd4b-1470ac95932f)

#### 3.3 Correlação e DTW

Em séries temporais, as variáveis podem parecer não correlacionadas em uma análise estática (como correlação de Pearson), mas ainda assim estarem sincronizadas em padrões temporais, com lags, compressões ou dilatações no tempo.O Dynamic Time Warping (DTW) resolve isso, permitindo medir a similaridade temporal não linear entre duas séries

📉 **Gráfico 3 — Clusterização DTW (Dendograma)**  
![Gráfico 3](https://github.com/user-attachments/assets/138252d0-a19a-449d-a572-f80adbcbfd4e)

O dendrograma mostra como variáveis com comportamentos temporais semelhantes (via DTW) podem ser agrupadas. Desta maneira podemos identificar variáveis redundantes (como VPact, VPdef, H2OC…)
A selecionar variáveis representativas de clusters para reduzir dimensionalidade sem perder informação relevante

#### 3.4 Seleção de Variáveis

**Tabela — Correlação de Pearson**

| Variáveis      | p (mbar) | Tpot (K) | rh (%)  | rho (g/m³) | wd (deg) | T (°C)  |
|----------------|----------|----------|---------|-------------|----------|---------|
| p (mbar)       | 1.000    | -0.164   | 0.043   | 0.354       | -0.089   | -0.080  |
| Tpot (K)       | -0.164   | 1.000    | -0.598  | -0.980      | -0.007   | 0.996   |
| rh (%)         | 0.043    | -0.598   | 1.000   | 0.551       | -0.018   | -0.601  |
| rho (g/m³)     | 0.354    | -0.980   | 0.551   | 1.000       | -0.014   | -0.960  |
| wd (deg)       | -0.089   | -0.007   | -0.018  | -0.014      | 1.000    | -0.015  |
| T (°C)         | -0.080   | 0.996    | -0.601  | -0.960      | -0.015   | 1.000   |

---

Mesmo que o DTW e o dendrograma mostrem variáveis com comportamentos temporais parecidos, ainda é necessário analisar a matriz de correlação para evitar colinearidade. Variáveis como Tpot (K) e T (°C) têm correlação de 0.996 — ou seja, carregam praticamente a mesma informação. Se usadas juntas num modelo, isso pode causar distorções nas estimativas. Por isso, DTW ajuda a entender padrões temporais, mas a correlação é essencial para garantir variáveis independentes entre si.

### 4. Modelagem e Avaliação

#### 4.1 Modelos Testados

Modelos simples como médias móveis e `naive` foram utilizados como benchmarks. Modelos mais complexos como LSTM e Prophet (com exógenas) também foram testados.

#### 4.2 Prevenção de Leakage

- Todas as variáveis foram defasadas em até 24h
- Nenhuma informação futura foi usada
- As últimas 24 horas foram reservadas como conjunto de teste
- Previsão em **passo único**, sem uso recursivo

#### 4.3 Resultados

**Tabela de Desempenho (MAE nas últimas 24h)**

| Modelo                                 | MAE (últimas 24h) |
|----------------------------------------|-------------------|
| **LSTM**                               | **0.99 °C**       |
| AutoARIMA                              | 1.55 °C           |
| Holt-Winters                           | 2.03 °C           |
| WindowAverage                          | 2.95 °C           |
| AutoARIMA (com exógenas)               | 3.50 °C           |
| Naive (últimos 2 dias)                 | 3.12 °C           |
| Naive (dezembro anterior)              | 6.24 °C           |
| Regressão Linear (com exógenas)        | 10.60 °C          |

---

Essa tabela compara o desempenho de diferentes modelos de previsão de temperatura nas últimas 24 horas, com base no erro médio absoluto (MAE). O modelo LSTM apresentou o melhor desempenho, seguido por AutoARIMA, enquanto abordagens mais simples como médias móveis (WindowAverage) e métodos ingênuos (Naive) tiveram erros maiores. Modelos com variáveis exógenas nem sempre melhoraram os resultados, destacando a complexidade adicional sem ganho claro em precisão.

**Gráfico 4.1 — Previsão de temperatura com LSTM**  
![image](https://github.com/user-attachments/assets/03795163-be2e-41a4-a9dc-902a7ea514a7)

O gráfico mostra como o modelo LSTM (linha laranja tracejada) conseguiu prever a temperatura nas últimas 24 horas com base em dados anteriores. A linha azul representa os valores reais, e vemos que o modelo conseguiu acompanhar bem os picos e quedas da temperatura — mostrando que ele aprendeu o padrão da série temporal.

**Gráfico 4.2 — Curva de Oerda do Modelo LSTM** 
![image](https://github.com/user-attachments/assets/f82ed2e1-b6b1-4805-98e6-aed463aef040)

Este gráfico mostra o erro do modelo durante o treinamento. A linha azul representa o erro nos dados de treino, e a laranja nos dados de validação. Ambas as curvas estão caindo, o que indica que o modelo está aprendendo e não está tendo overfitt. Desta maneira o  modelo LSTM aprendeu bem a prever a temperatura, com um erro baixo e comportamento estável durante o treino.  


### 5. Conclusão

O modelo **AutoArima** apresentou o melhor equilíbrio entre acurácia, interpretação e simplicidade. O **LSTM**, apesar de mais complexo, foi o mais preciso. A escolha depende da aplicação prática e da necessidade de interpretabilidade.

#### Melhorias Futuras:

- Explorar **modelos em conjunto (ensemble)**
- Reduzir frequência da série (média diária)
- Criar variáveis sazonais (hora, mês)
- Otimizar hiperparâmetros com validação cruzada
- Testar variáveis externas (altitude, latitude)
