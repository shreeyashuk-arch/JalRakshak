import os
import json
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

from edge_ai.datasets.synthetic_generator import generate_synthetic_dataset
from edge_ai.features.feature_extractor import extract_features_from_sample, FEATURE_NAMES

def train_and_evaluate_model():
    print("=" * 60)
    print("  JalRakshak: Edge-AI Baseline Model Training")
    print("  Classification Target: HEALTHY (0) / DEGRADING (1) / CRITICAL (2)")
    print("=" * 60)

    # 1. Ensure dataset exists
    data_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "synthetic_pump_dataset.json")
    if not os.path.exists(data_path):
        data_path = generate_synthetic_dataset()

    with open(data_path, "r") as f:
        data = json.load(f)

    # 2. Extract features
    X = []
    y = []
    for item in data:
        feats = extract_features_from_sample(
            item["vibration_series"],
            item["current_series"],
            item["temp_mean"],
            item["flow_mean"]
        )
        X.append(feats)
        y.append(item["health_state"])

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    # 3. Train compact Random Forest model suitable for export
    clf = RandomForestClassifier(n_estimators=20, max_depth=6, random_state=42)
    clf.fit(X_train, y_train)

    # 4. Evaluate
    y_pred = clf.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    report = classification_report(y_test, y_pred, target_names=["HEALTHY", "DEGRADING", "CRITICAL"], output_dict=True)

    print(f"\n[Evaluation] Measured Test Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    for cls_name in ["HEALTHY", "DEGRADING", "CRITICAL"]:
        print(f"  {cls_name:12s} - Precision: {report[cls_name]['precision']:.2f}, Recall: {report[cls_name]['recall']:.2f}, F1: {report[cls_name]['f1-score']:.2f}")

    # 5. Export Model & Metrics
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)

    model_path = os.path.join(models_dir, "baseline_pump_classifier.joblib")
    joblib.dump(clf, model_path)

    # Save metrics JSON
    metrics_path = os.path.join(os.path.dirname(__file__), "..", "evaluation", "evaluation_metrics.json")
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    with open(metrics_path, "w") as f:
        json.dump({
            "disclaimer": "These results are based on synthetic prototype data and do not represent field performance.",
            "test_accuracy": acc,
            "feature_names": FEATURE_NAMES,
            "report": report
        }, f, indent=2)

    print(f"\n[Export] Model saved to -> {model_path}")
    print(f"[Export] Metrics saved to -> {metrics_path}")
    return acc

if __name__ == "__main__":
    train_and_evaluate_model()
