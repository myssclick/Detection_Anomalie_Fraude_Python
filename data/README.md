# Données — UNSW-NB15

Les fichiers de données ne sont pas versionnés (voir `.gitignore`). Chaque membre doit les télécharger localement.

## Téléchargement

1. Aller sur la page officielle du dataset : https://research.unsw.edu.au/projects/unsw-nb15-dataset
2. Ouvrir le lien de téléchargement, puis le dossier **« Training and Testing Sets »**.
3. Télécharger les deux fichiers :
   - `UNSW_NB15_training-set.csv` (~175 000 lignes)
   - `UNSW_NB15_testing-set.csv` (~82 000 lignes)
4. Les placer dans `data/raw/` sans les renommer.

Arborescence attendue :

```
data/
├── raw/
│   ├── UNSW_NB15_training-set.csv
│   └── UNSW_NB15_testing-set.csv
└── processed/      # fichiers intermédiaires générés par le notebook
```

## Colonnes clés

| Colonne | Rôle |
|---|---|
| `id` | Identifiant de ligne — à exclure des features |
| `proto`, `service`, `state` | Variables catégorielles à encoder |
| `label` | 0 = normal, 1 = attaque — évaluation uniquement |
| `attack_cat` | Famille d'attaque (Normal, Fuzzers, Analysis, Backdoor, DoS, Exploits, Generic, Reconnaissance, Shellcode, Worms) — évaluation et construction des splits uniquement |

## Référence

Moustafa, N. & Slay, J. (2015). *UNSW-NB15: a comprehensive data set for network intrusion detection systems*. Military Communications and Information Systems Conference (MilCIS).
