import pytest
import os
import json
from edge_ai.datasets.synthetic_generator import generate_synthetic_dataset
from edge_ai.features.feature_extractor import extract_features_from_sample, FEATURE_NAMES
from edge_ai.inference.inference_engine import EdgeInferenceEngine

def test_dataset_generation():
    ds_path = generate_synthetic_dataset(samples_per_class=10)
    assert os.path.exists(ds_path)
    with open(ds_path, "r") as f:
        data = json.load(f)
    assert len(data) == 50
    assert "class_name" in data[0]

def test_feature_extraction():
    dummy_vib = [1.0] * 100
    dummy_curr = [4.2] * 100
    feats = extract_features_from_sample(dummy_vib, dummy_curr, 42.0, 85.0)
    assert len(feats) == len(FEATURE_NAMES)
    assert feats[0] == pytest.approx(1.0, 0.05) # RMS
    assert feats[8] == pytest.approx(1.0, 0.05) # Flow eff

def test_inference_engine():
    engine = EdgeInferenceEngine()
    # Healthy input
    res_healthy = engine.predict([1.0]*100, [4.2]*100, 42.0, 85.0)
    assert res_healthy["predicted_state"] in ["HEALTHY", "DEGRADING", "CRITICAL"]
    assert "health_score" in res_healthy
    assert "features" in res_healthy
