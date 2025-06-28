# ============================
# model.py
# ============================
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel
import numpy as np

def train_model(X_train, y_train, X_test, y_test):
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        eval_metric='logloss'
    )
    model.fit(X_train.values, y_train)

    selector = SelectFromModel(model, threshold="median", prefit=True)
    X_train_selected = selector.transform(X_train.values)
    X_test_selected = selector.transform(X_test.values)

    selected_feature_names = X_train.columns[selector.get_support()].tolist()
    print("Selected features:", selected_feature_names)

    model.fit(X_train_selected, y_train)
    probs = model.predict_proba(X_test_selected)[:, 1]
    y_pred = (probs > 0.6).astype(int)
    acc = accuracy_score(y_test, y_pred)
    return model, y_pred, acc
