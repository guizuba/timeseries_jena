from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model, X_train, X_test, y_train, y_test
