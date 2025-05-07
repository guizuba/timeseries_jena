# Jena Climate Temperature Forecast

Este projeto realiza a previsão da temperatura nas próximas 24 horas com base em dados meteorológicos. Utiliza Random Forest com engenharia de variáveis (lags) e avaliação com MAE.

---

## 🛠 Como Usar o Projeto

### 📁 Estrutura
- `src/`: scripts Python modularizados
- `notebooks/`: análises exploratórias
- `data/`: dataset original
- `main.py`: pipeline de execução completa

### ▶️ Execução
```bash
pip install -r requirements.txt
python main.py  ```


# Previsão de Temperatura com Séries Temporais Utilizando o Dataset Jena Climate

## 1. Introdução

A previsão de temperatura é um dos desafios centrais da meteorologia aplicada. A possibilidade de antecipar variações térmicas com precisão é crucial para setores como agricultura, energia, saúde e logística. Este estudo propõe a construção de um modelo preditivo capaz de estimar a temperatura nas próximas 24 horas, utilizando dados históricos do dataset Jena Climate. O desempenho dos modelos é avaliado com base na métrica de erro absoluto médio (MAE).

## 2. Metodologia

A tarefa de previsão de séries temporais envolve a análise de padrões históricos para estimar valores futuros. Para este fim, foram investigadas diferentes abordagens modelares, com ênfase na comparação entre métodos estatísticos clássicos e técnicas de aprendizado profundo. As categorias de modelos avaliadas incluem:

- **Modelos Lineares**: Regressão Linear;
- **Modelos de Séries Temporais**: ARIMA e ARIMAX;
- **Redes Neurais**: ANNs, RNNs e LSTM;
- **Modelos Baseados em Árvores de Decisão**;
- **Modelos Específicos para Séries Temporais**: Prophet, do Facebook.

Cada abordagem oferece diferentes capacidades em relação à captura de padrões sazonais, não linearidades e tendências de longo prazo.

## 3. Análise Exploratória dos Dados (EDA)

### 3.1 Tratamento de Valores Ausentes e Outliers

Foi identificado que as variáveis `wv` (velocidade do vento) e `max. wv` apresentavam valores `-9999.0`, representando dados faltantes. Esses valores foram substituídos por interpolação linear. Outliers extremos também foram suavizados.

**Gráfico 1 — Série Temporal da Temperatura**
![Gráfico 1](https://github.com/user-attachments/assets/41e29da2-364c-4b35-b897-7b83b049c95d)

### 3.2 Estatísticas Descritivas

A temperatura média observada foi de 9.44 °C, com variações entre -22.65 °C e 37.04 °C. A pressão atmosférica média foi de 989 mbar, com baixa variabilidade. Variáveis como `T (°C)`, `Tpot (K)`, `p (mbar)` e `rho (g/m³)` apresentaram distribuições aproximadamente normais, enquanto outras, como `VPdef`, `sh`, `H2OC` e `VPact`, exibiram distribuições assimétricas à direita. A direção do vento (`wd`) mostrou uma distribuição bimodal.

**Gráfico 2 — Distribuições das Variáveis**
![Gráfico 2](https://github.com/user-attachments/assets/70d58186-e2f2-43bc-bd4b-1470ac95932f)

### 3.3 Correlação e Similaridade Temporal

A correlação de Pearson mostrou que a temperatura está altamente correlacionada com `Tpot (K)`, `VPmax`, `sh` e `H2OC`, e negativamente correlacionada com `rho` e `rh`. Foi aplicada a métrica **Dynamic Time Warping (DTW)** para identificar similaridades temporais entre variáveis defasadas.

**Gráfico 3 — Clusterização com DTW**
![Gráfico 3](https://github.com/user-attachments/assets/138252d0-a19a-449d-a572-f80adbcbfd4e)

### 3.4 Seleção de Variáveis

Com base na matriz de distâncias DTW e correlações, selecionamos como preditoras: `p (mbar)`, `Tpot (K)`, `rh (%)`, `rho (g/m³)` e `wd (deg)`. A variável alvo foi `T (°C)`.

**Tabela 1 — Correlação de Pearson**

| Variáveis      | p (mbar) | Tpot (K) | rh (%)  | rho (g/m³) | wd (deg) | T (°C)  |
|----------------|----------|----------|---------|-------------|----------|---------|
| p (mbar)       | 1.000    | -0.164   | 0.043   | 0.354       | -0.089   | -0.080  |
| Tpot (K)       | -0.164   | 1.000    | -0.598  | -0.980      | -0.007   | 0.996   |
| rh (%)         | 0.043    | -0.598   | 1.000   | 0.551       | -0.018   | -0.601  |
| rho (g/m³)     | 0.354    | -0.980   | 0.551   | 1.000       | -0.014   | -0.960  |
| wd (deg)       | -0.089   | -0.007   | -0.018  | -0.014      | 1.000    | -0.015  |
| T (°C)         | -0.080   | 0.996    | -0.601  | -0.960      | -0.015   | 1.000   |

## 4. Modelagem e Avaliação

Durante a construção dos modelos, foi detectado **leakage** em `Tpot` e `rho`, pois essas variáveis são altamente derivadas da temperatura. Assim, foram excluídas do modelo final Prophet.

**Gráfico 4.1 — Modelos Simples**
![Gráfico 4.1](https://github.com/user-attachments/assets/6cb66549-7b12-4653-a0fc-d359bfab1218)

**Gráfico 4.2 — ARIMAX e Regressão com Exógenas**
![Gráfico 4.2](https://github.com/user-attachments/assets/9961d19e-a2e9-4272-bef6-c490b4879970)

**Gráfico 4.3 — Previsão com LSTM**
![Gráfico 4.3](https://github.com/user-attachments/assets/350a4475-3cd3-4247-a1db-53c86d4a59af)

**Gráfico 4.4 — Curva de Perda do LSTM**
![Gráfico 4.4](https://github.com/user-attachments/assets/eb0d5ae4-1b78-461b-a7d4-8c746d2085b1)

### Estratégia para Evitar Leakage

As variáveis foram defasadas (lags) em até 24 horas. Nenhuma informação futura foi utilizada. O modelo foi treinado apenas com dados históricos e testado nas últimas 24 horas. A previsão foi feita em passo único, sem alimentação recursiva.

### Tabela Comparativa de Modelos (MAE)

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

O modelo LSTM apresentou o melhor desempenho. Métodos mais simples e modelos com exógenas não superaram a versão com aprendizado profundo.

## 5. Discussão

A performance dos modelos variou conforme a abordagem de histórico adotada:

- **Histórico Curto (7 dias)**: responde rapidamente a mudanças, mas perde padrões sazonais;
- **Histórico Longo (3 anos)**: melhor captura de sazonalidade, porém com risco maior de overfitting.

## 6. Conclusão

O modelo Prophet com variáveis escolhidas via clusterização DTW apresentou o melhor equilíbrio entre **precisão**, **interpretação** e **complexidade**. Sugestões para versões futuras incluem:

- Combinação de modelos (ensemble);
- Redução de frequência da série (média diária);
- Criação de variáveis sazonais explícitas (hora/mês);
- Validação cruzada para ajuste de hiperparâmetros;
- Inclusão de variáveis externas (ex: latitude, altitude).

---

> _Este estudo reforça a importância da engenharia de variáveis e da seleção criteriosa de features para a construção de modelos robustos em previsão climática._
