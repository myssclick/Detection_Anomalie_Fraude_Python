"""Configuration commune : chemins, graine aléatoire et constantes du projet."""

import os
import random
from pathlib import Path

import numpy as np

# Graine unique utilisée dans toutes les expériences
RANDOM_STATE = 42

# Nombre de cœurs utilisés par les modèles qui le supportent (-1 = tous)
N_JOBS = -1

# Matériel pour XGBoost (classifieur supervisé de l'expérience 3) : "cuda" si GPU NVIDIA, sinon "cpu"
XGB_DEVICE = "cuda"

# Chemins
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
FIGURES_DIR = ROOT_DIR / "results" / "figures"
TABLES_DIR = ROOT_DIR / "results" / "tables"

# Fichiers UNSW-NB15 (version partitionnée officielle)
TRAIN_FILE = DATA_RAW_DIR / "UNSW_NB15_training-set.csv"
TEST_FILE = DATA_RAW_DIR / "UNSW_NB15_testing-set.csv"

# Colonnes du dataset
TARGET_COL = "label"            # 0 = normal, 1 = attaque
FAMILY_COL = "attack_cat"       # famille d'attaque ("Normal" pour le trafic normal)
ID_COL = "id"
CATEGORICAL_COLS = ["proto", "service", "state"]

# Niveaux de contamination de l'expérience 2
CONTAMINATION_LEVELS = [0.0, 0.01, 0.02, 0.05, 0.10]


def set_seed(seed: int = RANDOM_STATE) -> None:
    """Fixe les graines aléatoires (Python, NumPy) pour la reproductibilité."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
