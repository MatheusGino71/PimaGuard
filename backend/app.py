"""
PimaGuard - Sistema de Prevenção e Predição de Risco de Diabetes Tipo 2
Backend em FastAPI com Machine Learning, SHAP e Explicabilidade
"""

import os
import zipfile
import warnings
from pathlib import Path
from typing import List, Optional

import joblib
import kagglehub
import numpy as np
import pandas as pd
import shap
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

app = FastAPI(
    title="PimaGuard API",
    description="Sistema de Predição de Risco de Diabetes Tipo 2",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# ============================================================================
# MODELOS PYDANTIC
# ============================================================================


class PredictionInput(BaseModel):
    """Modelo de entrada para predição"""

    pregnancies: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree_function: float
    age: float


class RiskFactor(BaseModel):
    """Modelo de fator de risco"""

    feature: str
    impact_value: float
    impact_percentage: float


class PredictionOutput(BaseModel):
    """Modelo de saída para predição"""

    diabetes_risk_percentage: float
    risk_level: str
    risk_factors: List[RiskFactor]
    model_used: str
    confidence: float


# ============================================================================
# PIPELINE DE DADOS E ML
# ============================================================================


class PimaMLPipeline:
    """Pipeline completo de ML para Diabetes"""

    def __init__(self):
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.model_rf = None
        self.model_lr = None
        self.explainer_rf = None
        self.explainer_lr = None
        self.feature_names = None
        self.dataset_summary = None
        self.monitoring_summary = None
        self.data_is_scaled = False

    def _load_csv_from_zip(self, zip_path):
        extract_dir = DATA_DIR / "kaggle_extract"
        extract_dir.mkdir(exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        csv_path = next(extract_dir.rglob("*.csv"), None)
        if csv_path is None:
            raise RuntimeError("Arquivo CSV não encontrado dentro do zip do dataset.")
        return pd.read_csv(csv_path)

    def download_dataset(self):
        """Download automático do dataset Pima"""
        print("Baixando dataset Pima Indians Diabetes...")
        try:
            local_zip = next(DATA_DIR.glob("*.zip"), None)
            if local_zip is not None:
                self.df = self._load_csv_from_zip(local_zip)
                print(f"Dataset carregado do zip local. Shape: {self.df.shape}")
                return self.df

            root_zip = BASE_DIR.parent / "archive.zip"
            if root_zip.exists():
                self.df = self._load_csv_from_zip(root_zip)
                print(f"Dataset carregado do archive.zip local. Shape: {self.df.shape}")
                return self.df

            dataset_path = kagglehub.dataset_download("uciml/pima-indians-diabetes-database")
            csv_path = next(Path(dataset_path).rglob("*.csv"), None)
            if csv_path is None:
                raise RuntimeError("Nenhum arquivo CSV foi encontrado no dataset baixado do Kaggle.")

            self.df = pd.read_csv(csv_path)
            print(f"Dataset baixado com sucesso. Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            raise RuntimeError(
                "Não foi possível baixar o dataset do Kaggle com kagglehub. "
                "Configure o acesso ao Kaggle e tente novamente."
            ) from e

    def prepare_data(self):
        """Preparação e limpeza dos dados"""
        print("Preparando dados...")

        if self.df is None:
            raise ValueError("Dataset não foi carregado!")

        # Tratamento de valores ausentes (zeros inválidos)
        columns_with_zeros = [
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
        ]

        for col in columns_with_zeros:
            if col in self.df.columns:
                # Substituir zeros por mediana (mais robusto)
                self.df[col] = self.df[col].replace(0, self.df[col].median())

        # Separar features e target
        self.feature_names = [col for col in self.df.columns if col != "Outcome"]
        self.X = self.df[self.feature_names].values
        self.y = self.df["Outcome"].values

        print(f"✓ Features: {self.feature_names}")
        print(f"✓ Classes: {np.unique(self.y)}")
        print(f"✓ Data preparada: X shape {self.X.shape}, y shape {self.y.shape}")

    def build_dataset_summary(self):
        """Montar métricas do dataset para o dashboard"""
        if self.df is None:
            raise ValueError("Dataset não foi carregado!")

        summary_df = self.df.copy()
        class_counts = summary_df["Outcome"].value_counts().sort_index()

        self.dataset_summary = {
            "rows": int(len(summary_df)),
            "features": int(len(self.feature_names)) if self.feature_names else 0,
            "class_balance": {
                "negative": int(class_counts.get(0, 0)),
                "positive": int(class_counts.get(1, 0)),
            },
            "positive_rate": round(float(summary_df["Outcome"].mean() * 100), 2),
            "feature_means": {
                "Glucose": round(float(summary_df["Glucose"].mean()), 2),
                "BMI": round(float(summary_df["BMI"].mean()), 2),
                "Age": round(float(summary_df["Age"].mean()), 2),
                "BloodPressure": round(float(summary_df["BloodPressure"].mean()), 2),
            },
            "feature_medians": {
                "Glucose": round(float(summary_df["Glucose"].median()), 2),
                "BMI": round(float(summary_df["BMI"].median()), 2),
                "Age": round(float(summary_df["Age"].median()), 2),
            },
            "missing_values": int(summary_df.isna().sum().sum()),
            "zero_replacements": {
                "Glucose": int((self.df["Glucose"] == 0).sum()) if "Glucose" in self.df.columns else 0,
                "BloodPressure": int((self.df["BloodPressure"] == 0).sum()) if "BloodPressure" in self.df.columns else 0,
                "SkinThickness": int((self.df["SkinThickness"] == 0).sum()) if "SkinThickness" in self.df.columns else 0,
                "Insulin": int((self.df["Insulin"] == 0).sum()) if "Insulin" in self.df.columns else 0,
                "BMI": int((self.df["BMI"] == 0).sum()) if "BMI" in self.df.columns else 0,
            },
        }

    def build_monitoring_summary(self):
        """Montar métricas de monitoramento dos modelos"""
        if self.X_test is None or self.y_test is None:
            raise ValueError("Conjunto de teste não foi preparado!")

        X_eval = self.X_test if self.data_is_scaled else self.scaler.transform(self.X_test)
        monitoring = {
            "selected_model": self.best_model_name,
            "test_samples": int(len(self.y_test)),
            "models": {},
            "feature_importance": {},
            "class_distribution": {
                "negative": int((self.y_test == 0).sum()),
                "positive": int((self.y_test == 1).sum()),
            },
        }

        for model, name in [
            (self.model_rf, "Random Forest"),
            (self.model_lr, "Regressão Logística"),
        ]:
            y_pred = model.predict(X_eval)
            y_proba = model.predict_proba(X_eval)[:, 1]
            tn, fp, fn, tp = confusion_matrix(self.y_test, y_pred).ravel()

            monitoring["models"][name] = {
                "accuracy": round(float(accuracy_score(self.y_test, y_pred) * 100), 2),
                "auc": round(float(roc_auc_score(self.y_test, y_proba) * 100), 2),
                "precision": round(float(precision_score(self.y_test, y_pred, zero_division=0) * 100), 2),
                "recall": round(float(recall_score(self.y_test, y_pred, zero_division=0) * 100), 2),
                "f1": round(float(f1_score(self.y_test, y_pred, zero_division=0) * 100), 2),
                "confusion_matrix": {
                    "tn": int(tn),
                    "fp": int(fp),
                    "fn": int(fn),
                    "tp": int(tp),
                },
            }

        feature_importances = getattr(self.model_rf, "feature_importances_", None)
        if feature_importances is not None:
            ranked_features = sorted(
                zip(self.feature_names, feature_importances),
                key=lambda item: item[1],
                reverse=True,
            )[:5]
            monitoring["feature_importance"] = {
                feature: round(float(score * 100), 2)
                for feature, score in ranked_features
            }

        self.monitoring_summary = monitoring

    def split_data(self, test_size=0.2, random_state=42):
        """Divisão treino/teste"""
        print("✂️  Dividindo dados em treino/teste...")
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y,
        )
        self.data_is_scaled = False
        print(f"✓ Treino: {self.X_train.shape[0]} | Teste: {self.X_test.shape[0]}")

    def scale_features(self):
        """Normalização de features"""
        print("Normalizando features...")
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        self.data_is_scaled = True
        print("✓ Features normalizadas")

    def train_models(self):
        """Treinamento de 2 modelos de classificação"""
        print("\nTreinando modelos...")

        # 1. Random Forest
        print("  1. Treinando Random Forest...")
        self.model_rf = RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
        )
        self.model_rf.fit(self.X_train, self.y_train)
        rf_score = self.model_rf.score(self.X_test, self.y_test)
        print(f"     ✓ Random Forest - Acurácia: {rf_score:.4f}")

        # 2. Regressão Logística
        print("  2. Treinando Regressão Logística...")
        self.model_lr = LogisticRegression(max_iter=1000, random_state=42)
        self.model_lr.fit(self.X_train, self.y_train)
        lr_score = self.model_lr.score(self.X_test, self.y_test)
        print(f"     ✓ Regressão Logística - Acurácia: {lr_score:.4f}")

        # Usar o melhor modelo
        self.best_model = self.model_rf if rf_score >= lr_score else self.model_lr
        self.best_model_name = (
            "Random Forest" if rf_score >= lr_score else "Regressão Logística"
        )

        print(f"\nModelo selecionado: {self.best_model_name}")

    def evaluate_models(self):
        """Avaliação detalhada dos modelos"""
        print("\nAvaliando modelos...\n")

        for model, name in [
            (self.model_rf, "Random Forest"),
            (self.model_lr, "Regressão Logística"),
        ]:
            y_pred = model.predict(self.X_test)
            y_proba = model.predict_proba(self.X_test)[:, 1]

            print(f"{'=' * 60}")
            print(f"  {name}")
            print(f"{'=' * 60}")
            print(f"Acurácia: {model.score(self.X_test, self.y_test):.4f}")
            print(f"AUC-ROC: {roc_auc_score(self.y_test, y_proba):.4f}")
            print(f"\nRelatório de Classificação:\n")
            print(
                classification_report(
                    self.y_test, y_pred, target_names=["Sem Diabetes", "Com Diabetes"]
                )
            )

    def create_explainers(self):
        """Criar explainers SHAP para cada modelo"""
        print("\nCriando explainers SHAP...")

        # Usar amostra dos dados de treino para SHAP (mais rápido)
        X_sample = self.X_train[:100]

        print("  ▪ SHAP para Random Forest...")
        self.explainer_rf = shap.TreeExplainer(self.model_rf)

        print("  ▪ SHAP para Regressão Logística...")
        self.explainer_lr = shap.KernelExplainer(
            self.model_lr.predict_proba, shap.sample(X_sample, 50)
        )

        print("✓ Explainers SHAP criados")

    def save_pipeline(self):
        """Salvar modelos e pipeline"""
        print("\nSalvando modelos...")
        joblib.dump(self.model_rf, MODELS_DIR / "model_random_forest.pkl")
        joblib.dump(self.model_lr, MODELS_DIR / "model_logistic_regression.pkl")
        joblib.dump(self.scaler, MODELS_DIR / "scaler.pkl")
        joblib.dump(self.feature_names, MODELS_DIR / "feature_names.pkl")
        print("✓ Modelos salvos")

    def load_pipeline(self):
        """Carregar modelos salvos"""
        try:
            print("Carregando modelos...")
            self.model_rf = joblib.load(MODELS_DIR / "model_random_forest.pkl")
            self.model_lr = joblib.load(MODELS_DIR / "model_logistic_regression.pkl")
            self.scaler = joblib.load(MODELS_DIR / "scaler.pkl")
            self.feature_names = joblib.load(MODELS_DIR / "feature_names.pkl")
            self.best_model = self.model_rf
            self.best_model_name = "Random Forest"
            self.explainer_rf = shap.TreeExplainer(self.model_rf)
            print("✓ Modelos carregados com sucesso")
            return True
        except:
            print("Não foi possível carregar modelos salvos")
            return False

    def predict_with_explanation(self, X_input):
        """
        Fazer predição com explicação SHAP

        Args:
            X_input: Array com [pregnancies, glucose, blood_pressure, skin_thickness,
                               insulin, bmi, diabetes_pedigree_function, age]

        Returns:
            Tuple (probabilidade, fatores_risco)
        """
        # Normalizar input
        X_scaled = self.scaler.transform([X_input])

        # Predição
        prediction = self.best_model.predict(X_scaled)[0]
        probability = self.best_model.predict_proba(X_scaled)[0][1]

        # SHAP values
        if self.best_model_name == "Random Forest":
            if self.explainer_rf is None:
                self.explainer_rf = shap.TreeExplainer(self.model_rf)
            shap_output = self.explainer_rf.shap_values(X_scaled)
            if isinstance(shap_output, list):
                shap_values = shap_output[1][0] if len(shap_output) > 1 else shap_output[0][0]
            else:
                shap_values = shap_output[0]
        else:
            if self.explainer_lr is None:
                self.explainer_lr = shap.Explainer(self.model_lr, self.X_train[:50])
            shap_output = self.explainer_lr(X_scaled)
            shap_values = shap_output.values[0]

        # Ordenar features por impacto
        risk_factors = []
        for i, (feature, shap_val) in enumerate(zip(self.feature_names, shap_values)):
            risk_factors.append(
                {
                    "feature": feature,
                    "shap_value": float(shap_val),
                    "impact": abs(float(shap_val)),
                }
            )

        # Ordenar e pegar top 5
        risk_factors = sorted(risk_factors, key=lambda x: x["impact"], reverse=True)[:5]

        return probability, risk_factors


# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

# Instância global do pipeline
pipeline = PimaMLPipeline()


def initialize_pipeline():
    """Inicializar pipeline na startup"""
    print("\n" + "=" * 70)
    print("  PimaGuard - Sistema de Prevenção de Diabetes Tipo 2")
    print("=" * 70 + "\n")

    # Tentar carregar modelos existentes
    if pipeline.load_pipeline():
        if pipeline.dataset_summary is None:
            pipeline.download_dataset()
            pipeline.prepare_data()
            pipeline.split_data()
            pipeline.build_dataset_summary()
            pipeline.build_monitoring_summary()
        return

    # Se não existir, treinar novo
    pipeline.download_dataset()
    pipeline.prepare_data()
    pipeline.build_dataset_summary()
    pipeline.split_data()
    pipeline.scale_features()
    pipeline.train_models()
    pipeline.evaluate_models()
    pipeline.build_monitoring_summary()
    pipeline.create_explainers()
    pipeline.save_pipeline()

    print("\nPipeline inicializado com sucesso!\n")


# ============================================================================
# ROTAS API
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Evento de inicialização"""
    initialize_pipeline()


@app.get("/", tags=["Health"])
async def root():
    """Rota raiz - Health check"""
    return {
        "status": "online",
        "app": "PimaGuard API",
        "version": "1.0.0",
        "message": "Sistema de Prevenção e Predição de Risco de Diabetes Tipo 2",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "models_loaded": pipeline.model_rf is not None,
        "scaler_ready": pipeline.scaler is not None,
        "features_count": len(pipeline.feature_names) if pipeline.feature_names else 0,
    }


@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
async def predict(input_data: PredictionInput):
    """
    Predizer risco de Diabetes Tipo 2

    Recebe dados do paciente e retorna:
    - Percentual de risco
    - Nível de risco (Baixo, Moderado, Alto, Muito Alto)
    - Principais fatores de risco (SHAP)
    """
    try:
        # Preparar input
        X_input = np.array(
            [
                input_data.pregnancies,
                input_data.glucose,
                input_data.blood_pressure,
                input_data.skin_thickness,
                input_data.insulin,
                input_data.bmi,
                input_data.diabetes_pedigree_function,
                input_data.age,
            ]
        )

        # Predição com explicação
        probability, risk_factors = pipeline.predict_with_explanation(X_input)

        # Determinar nível de risco
        if probability < 0.25:
            risk_level = "Baixo"
        elif probability < 0.50:
            risk_level = "Moderado"
        elif probability < 0.75:
            risk_level = "Alto"
        else:
            risk_level = "Muito Alto"

        # Calcular impacto normalizado
        total_impact = sum(rf["impact"] for rf in risk_factors)
        risk_factors_output = [
            RiskFactor(
                feature=rf["feature"],
                impact_value=float(rf["shap_value"]),
                impact_percentage=float(
                    (rf["impact"] / total_impact * 100) if total_impact > 0 else 0
                ),
            )
            for rf in risk_factors
        ]

        return PredictionOutput(
            diabetes_risk_percentage=round(probability * 100, 2),
            risk_level=risk_level,
            risk_factors=risk_factors_output,
            model_used=pipeline.best_model_name,
            confidence=round(
                max(
                    pipeline.best_model.predict_proba(
                        pipeline.scaler.transform([X_input])
                    )[0]
                )
                * 100,
                2,
            ),
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na predição: {str(e)}")


@app.get("/info", tags=["Information"])
async def info():
    """Informações sobre o modelo e dataset"""
    return {
        "model": pipeline.best_model_name,
        "features": pipeline.feature_names,
        "features_count": len(pipeline.feature_names) if pipeline.feature_names else 0,
        "training_samples": len(pipeline.X_train)
        if pipeline.X_train is not None
        else 0,
        "test_samples": len(pipeline.X_test) if pipeline.X_test is not None else 0,
        "risk_levels": [
            "Baixo (< 25%)",
            "Moderado (25-50%)",
            "Alto (50-75%)",
            "Muito Alto (> 75%)",
        ],
    }


@app.get("/dataset-summary", tags=["Information"])
async def dataset_summary():
    """Resumo estatístico do dataset para dashboards do frontend"""
    if pipeline.dataset_summary is None:
        raise HTTPException(status_code=503, detail="Resumo do dataset ainda não está disponível")
    return pipeline.dataset_summary


@app.get("/monitoring-summary", tags=["Information"])
async def monitoring_summary():
    """Resumo de monitoramento dos modelos para dashboards do frontend"""
    if pipeline.monitoring_summary is None:
        raise HTTPException(status_code=503, detail="Resumo de monitoramento ainda não está disponível")
    return pipeline.monitoring_summary


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("\nIniciando servidor PimaGuard...\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
