# Detection_Anomalie_Fraude_Python

Projet 5 du cours de Détection d'Anomalies et Fraude en Python — **Détection d'attaques inconnues par Anomaly Detection**.

> **Question centrale :** peut-on détecter des attaques inconnues sans disposer d'exemples de ces attaques pendant l'entraînement ?

- **Dataset :** UNSW-NB15
- **Démarche :** voir [roadmap.md](roadmap.md)
- **Sujet :** [Projet5.pdf](Projet5.pdf)

## Structure du dépôt

```
data/
  raw/            # CSV UNSW-NB15 (versionnés, voir data/README.md)
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

Les données sont récupérées avec le `git clone`.

### 2. Données

Les fichiers `UNSW_NB15_training-set.csv` et `UNSW_NB15_testing-set.csv` sont inclus dans le dépôt (`data/raw/`) : rien à télécharger. Source et description des colonnes : [data/README.md](data/README.md).

### 3. Exécution

Ouvrir [notebooks/projet5_anomaly_detection.ipynb](notebooks/projet5_anomaly_detection.ipynb) et exécuter toutes les cellules dans l'ordre (*Restart & Run All*).

## Dataset et citations

Ce projet utilise le dataset **UNSW-NB15** ([page officielle](https://research.unsw.edu.au/projects/unsw-nb15-dataset)). Ses auteurs demandent que toute utilisation cite les deux articles suivants :

1. Moustafa, Nour, and Jill Slay. "UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set)." *Military Communications and Information Systems Conference (MilCIS), 2015*. IEEE, 2015.
2. Moustafa, Nour, and Jill Slay. "The evaluation of Network Anomaly Detection Systems: Statistical analysis of the UNSW-NB15 data set and the comparison with the KDD99 data set." *Information Security Journal: A Global Perspective* (2016): 1-14.

Ces deux références doivent aussi figurer dans la bibliographie du rapport.

## Reproductibilité

- Graine aléatoire unique : `RANDOM_STATE = 42` (définie dans [src/config.py](src/config.py)).
- Versions des bibliothèques figées dans [requirements.txt](requirements.txt) et affichées en début de notebook.
