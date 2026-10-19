import os
import joblib
import numpy as np
from edge_ai.features.feature_extractor import extract_features_from_sample

class EdgeInferenceEngine:
    """
    Offline-capable inference engine mapping raw sensor series to
    state classification (HEALTHY, DEGRADING, CRITICAL) and anomaly metrics.
    """
    STATE_LABELS = {0: "HEALTHY", 1: "DEGRADING", 2: "CRITICAL"}

    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "..", "models", "baseline_pump_classifier.joblib")
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = None

    def predict(self, vib_series, current_series, temp_val, flow_val):
        feats = extract_features_from_sample(vib_series, current_series, temp_val, flow_val)
        
        if self.model is not None:
            pred_class = int(self.model.predict([feats])[0])
            probs = self.model.predict_proba([feats])[0]
            confidence = float(np.max(probs))
            anomaly_score = float(1.0 - probs[0]) # distance from healthy class
        else:
            # Fallback algorithmic heuristic if model file is absent
            vib_rms = feats[0]
            if vib_rms < 1.25 and temp_val < 50:
                pred_class = 0
            elif vib_rms < 1.70:
                pred_class = 1
            else:
                pred_class = 2
            confidence = 0.90
            anomaly_score = 0.15 if pred_class == 0 else (0.55 if pred_class == 1 else 0.90)

        # Health percentage mapping
        health_pct = max(10.0, min(100.0, 100.0 * (1.0 - anomaly_score)))

        return {
            "predicted_state": self.STATE_LABELS[pred_class],
            "state_id": pred_class,
            "health_score": round(health_pct, 1),
            "anomaly_score": round(anomaly_score, 3),
            "confidence": round(confidence, 3),
            "features": {
                "vibration_rms": round(feats[0], 3),
                "crest_factor": round(feats[3], 2),
                "current_rms": round(feats[4], 2),
                "temperature": round(feats[6], 1),
                "flow_efficiency": round(feats[8], 2)
            }
        }
