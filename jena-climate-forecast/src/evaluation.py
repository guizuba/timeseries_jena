from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'MAE: {mae:.2f}')
    return y_test, y_pred, mae

def plot_predictions(y_test, y_pred):
    plt.figure(figsize=(12, 4))
    plt.plot(y_test[:144], label="Real")
    plt.plot(y_pred[:144], label="Previsto")
    plt.legend()
    plt.title("Previsão de Temperatura nas Próximas 24h")
    plt.xlabel("Hora")
    plt.ylabel("Temperatura (°C)")
    plt.tight_layout()
    plt.show()
