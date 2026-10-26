# Données — UNSW-NB15

Les fichiers du dataset sont versionnés dans `data/raw/` : un `git clone` suffit, aucun téléchargement n'est nécessaire.

```
data/
├── raw/
│   ├── UNSW_NB15_training-set.csv   # 175 341 lignes
│   ├── UNSW_NB15_testing-set.csv    #  82 332 lignes
│   └── NUSW-NB15_features.csv       # description des variables
└── processed/      # fichiers intermédiaires générés par le notebook (non versionnés)
```

## Source

Fichiers récupérés sur la page officielle du dataset : https://research.unsw.edu.au/projects/unsw-nb15-dataset
(lien de téléchargement > **CSV Files** > dossier **« Training and Testing Sets »**, et `NUSW-NB15_features.csv` dans **CSV Files**).

## Colonnes clés

| Colonne | Rôle |
|---|---|
| `id` | Identifiant de ligne — à exclure des features |
| `proto`, `service`, `state` | Variables catégorielles à encoder |
| `label` | 0 = normal, 1 = attaque — évaluation uniquement |
| `attack_cat` | Famille d'attaque (Normal, Fuzzers, Analysis, Backdoor, DoS, Exploits, Generic, Reconnaissance, Shellcode, Worms) — évaluation et construction des splits uniquement |

## Citations obligatoires

Les auteurs du dataset demandent de citer deux articles : voir la section « Dataset et citations » du [README principal](../README.md).
