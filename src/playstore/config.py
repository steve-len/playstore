import os.path


PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
CLEAN_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")
MODEL_DIR = os.path.join(PROJECT_ROOT, "data", "model")