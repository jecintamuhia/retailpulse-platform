import xgboost as xgb
import shap
import pandas as pd
from sklearn.model_selection import train_test_split
def execute_explainable_churn_training(rfm_df: pd.DataFrame):
X = rfm_df[["Recency", "Frequency", "Monetary"]]
y = rfm_df["is_churned"]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y,
random_state=42)
model = xgb.XGBClassifier(n_estimators=300, max_depth=5, learning_rate=0.05,
eval_metric="logloss")
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_val)
return model, shap_values