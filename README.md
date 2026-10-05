# Detection_Anomalie_Fraude_Python

Projet 5 du cours de Détection d'Anomalies et Fraude en Python — **Détection d'attaques inconnues par Anomaly Detection**.

> **Question centrale :** peut-on détecter des attaques inconnues sans disposer d'exemples de ces attaques pendant l'entraînement ?

- **Dataset :** UNSW-NB15
- **Démarche :** voir [roadmap.md](roadmap.md)
- **Sujet :** [Projet5.pdf](Projet5.pdf)

## Structure du dépôt

```
data/
  raw/            # CSV UNSW-NB15 (non versionnés, voir data/README.md)
  processed/      # données intermédiaires générées
notebooks/        # notebook principal du projet
src/              # code réutilisable (config, preprocessing, métriques, figures)
results/
  figures/        # figures générées par le notebook
  tables/         # tableaux de résultats (CSV)
report/           # rapport et présentation
requirements.txt
roadmap.md
```

## Reproduire les expériences

### 1. Installation (en local)

Prérequis : Python ≥ 3.12.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 1 bis. Installation (Google Colab)

```python
!git clone https://github.com/myssclick/Detection_Anomalie_Fraude_Python.git
%cd Detection_Anomalie_Fraude_Python
!pip install -r requirements.txt
```

Puis déposer les CSV dans `data/raw/` (upload ou Google Drive).

### 2. Données

Télécharger les fichiers `UNSW_NB15_training-set.csv` et `UNSW_NB15_testing-set.csv` et les placer dans `data/raw/` — instructions détaillées dans [data/README.md](data/README.md).

### 3. Exécution

Ouvrir [notebooks/projet5_anomaly_detection.ipynb](notebooks/projet5_anomaly_detection.ipynb) et exécuter toutes les cellules dans l'ordre (*Restart & Run All*).

## Reproductibilité

- Graine aléatoire unique : `RANDOM_STATE = 42` (définie dans [src/config.py](src/config.py)).
- Versions des bibliothèques figées dans [requirements.txt](requirements.txt) et affichées en début de notebook.
