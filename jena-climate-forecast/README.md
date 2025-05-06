# Jena Climate Temperature Forecast

Este projeto realiza a previsão da temperatura nas próximas 24 horas com base em dados meteorológicos. Utiliza Random Forest com engenharia de variáveis (lags) e avaliação com MAE.

## Estrutura do Projeto
- `src/`: scripts Python modularizados
- `notebooks/`: análises exploratórias
- `data/`: dataset original
- `main.py`: pipeline de execução completa

## Como Rodar
```bash
pip install -r requirements.txt
python main.py
