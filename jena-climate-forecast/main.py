from src.preprocessing import load_data, handle_missing_values, scale_features
from src.feature_engineering import create_lagged_features
from src.model_training import train_model
from src.evaluation import evaluate_model, plot_predictions

df = load_data('data/jena_climate_2009_2016.csv')
df = handle_missing_values(df)
features = [col for col in df.columns if col not in ['Date Time']]
df = scale_features(df, features)

df = create_lagged_features(df, target='T (degC)', n_lags=144)
X = df.drop(columns=['T (degC)', 'Date Time'])
y = df['T (degC)']

model, X_train, X_test, y_train, y_test = train_model(X, y)
y_test, y_pred, mae = evaluate_model(model, X_test, y_test)
plot_predictions(y_test, y_pred)
