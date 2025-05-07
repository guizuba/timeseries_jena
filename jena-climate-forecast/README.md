
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

- Temperatura média: 9.44 °C
- Pressão média: 989 mbar (±8.3)
- Variáveis `T`, `Tpot`, `p`, `rho` seguem distribuição normal
- Outras, como `VPact`, `sh`, `max. wv`, têm cauda longa à direita
- `wd` tem distribuição bimodal

📊 **Gráfico 2 — Distribuições das Variáveis**  
![Gráfico 2](https://github.com/user-attachments/assets/70d58186-e2f2-43bc-bd4b-1470ac95932f)

#### 3.3 Correlação e DTW

- `T` correlaciona fortemente com `Tpot`, `sh`, `VPmax`, `H2OC`
- Correlação negativa com `rho` (-0.96) e `rh` (-0.57)
- DTW foi aplicado para medir similaridade temporal entre variáveis com lags

📉 **Gráfico 3 — Clusterização DTW (Dendograma)**  
![Gráfico 3](https://github.com/user-attachments/assets/138252d0-a19a-449d-a572-f80adbcbfd4e)

#### 3.4 Seleção de Variáveis

A partir da análise de correlação e DTW, foram escolhidas:

- `p (mbar)`
- `Tpot (K)`
- `rh (%)`
- `rho (g/m³)`
- `wd (deg)`

A variável alvo foi `T (°C)`.

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

### 5. Discussão

As estratégias de seleção de histórico influenciam diretamente a performance:

- **Histórico curto (7 dias)**: capta mudanças recentes, mas perde sazonalidade;
- **Histórico longo (3 anos)**: favorece a sazonalidade, mas pode causar overfitting.

Modelos como LSTM apresentaram excelente desempenho, superando abordagens estatísticas clássicas.

---

### 6. Conclusão

O modelo **Prophet** com variáveis selecionadas via **clusterização DTW** apresentou o melhor equilíbrio entre acurácia, interpretação e simplicidade. O **LSTM**, apesar de mais complexo, foi o mais preciso. A escolha depende da aplicação prática e da necessidade de interpretabilidade.

#### Melhorias Futuras:

- Explorar **modelos em conjunto (ensemble)**
- Reduzir frequência da série (média diária)
- Criar variáveis sazonais (hora, mês)
- Otimizar hiperparâmetros com validação cruzada
- Testar variáveis externas (altitude, latitude)
