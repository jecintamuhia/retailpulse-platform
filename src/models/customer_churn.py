import xgboost as xgb
import shap
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score


def execute_explainable_churn_training(rfm_df: pd.DataFrame):
    # --- Features (expanded)
    feature_cols = [
        "Recency",
        "Frequency",
        "Monetary",
        "avg_order_value",
        "total_items",
        "unique_products",
    ]

    X = rfm_df[feature_cols]
    y = rfm_df["is_churned"]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        eval_metric="logloss",
        use_label_encoder=False,
    )

    model.fit(X_train, y_train)

    # --- Evaluation
    preds = model.predict(X_val)
    probs = model.predict_proba(X_val)[:, 1]

    print("\n📊 Model Performance")
    print(classification_report(y_val, preds))
    print("ROC-AUC:", roc_auc_score(y_val, probs))

    # --- SHAP explainability
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_val)

    return model, shap_values