import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline

# Simulated sensor data generation
def generate_sensor_data(num_samples):
    data = {
        'Sensor1': np.random.rand(num_samples),
        'Sensor2': np.random.rand(num_samples),
        'Sensor3': np.random.rand(num_samples),
        'Sensor4': np.random.rand(num_samples),
        'Sensor5': np.random.rand(num_samples),
        'Fault': np.random.randint(2, size=num_samples),  # Binary fault indicator (0: No Fault, 1: Fault)
    }
    return pd.DataFrame(data)

# Feature engineering
def feature_engineering(X, y):
    # Standard scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Principal Component Analysis (PCA)
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_scaled)

    # Feature selection using SelectKBest
    selector = SelectKBest(f_classif, k=2)
    X_selected = selector.fit_transform(X_pca, y)

    return X_selected

# Model training
def train_model(X, y):
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X, y)
    return rf_classifier

# Evaluation
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report

# Main function
def main():
    # Generate and split the dataset
    num_samples = 1000
    sensor_data = generate_sensor_data(num_samples)
    X = sensor_data.drop('Fault', axis=1)
    y = sensor_data['Fault']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Feature engineering
    X_train_fe = feature_engineering(X_train, y_train)
    X_test_fe = feature_engineering(X_test, y_test)

    # Model training
    model = train_model(X_train_fe, y_train)

    # Evaluation
    accuracy, report = evaluate_model(model, X_test_fe, y_test)
    print(f'Accuracy: {accuracy:.2f}')
    print('Classification Report:')
    print(report)

    # Predict faults for new sensor data
    new_sensor_data = generate_sensor_data(5)
    new_sensor_data_fe = feature_engineering(new_sensor_data.drop('Fault', axis=1), [])
    predicted_faults = model.predict(new_sensor_data_fe)
    print('Predicted Faults for New Sensor Data:')
    for i, fault in enumerate(predicted_faults):
        print(f'Sensor {i + 1}: {"Fault" if fault == 1 else "No Fault"}')

if __name__ == '__main__':
    main()
