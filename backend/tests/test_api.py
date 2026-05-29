VALID_PAYLOAD = {
    "pregnancies": 1,
    "glucose": 120,
    "blood_pressure": 70,
    "skin_thickness": 20,
    "insulin": 30,
    "bmi": 25,
    "diabetes_pedigree_function": 0.5,
    "age": 30,
}


def test_health_endpoint_returns_ready_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models_loaded"] is True
    assert data["scaler_ready"] is True
    assert data["features_count"] == 8


def test_predict_endpoint_returns_risk_and_explanations(client):
    response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert "diabetes_risk_percentage" in data
    assert "risk_level" in data
    assert "risk_factors" in data
    assert "model_used" in data
    assert "confidence" in data
    assert isinstance(data["risk_factors"], list)
    assert len(data["risk_factors"]) > 0


def test_predict_endpoint_rejects_missing_fields(client):
    response = client.post("/predict", json={"glucose": 120})

    assert response.status_code == 422


def test_dataset_summary_endpoint_returns_dashboard_data(client):
    response = client.get("/dataset-summary")

    assert response.status_code == 200
    data = response.json()
    assert data["rows"] > 0
    assert data["features"] == 8
    assert "class_balance" in data
    assert "feature_means" in data


def test_monitoring_summary_endpoint_returns_model_metrics(client):
    response = client.get("/monitoring-summary")

    assert response.status_code == 200
    data = response.json()
    assert data["selected_model"] in {"Random Forest", "Regressão Logística"}
    assert data["test_samples"] > 0
    assert "models" in data
    assert "Random Forest" in data["models"]
    assert "Regressão Logística" in data["models"]
