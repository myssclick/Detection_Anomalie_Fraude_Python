# Roadmap — Projet 5 : Détection d'attaques inconnues par Anomaly Detection

> **Question centrale :** Peut-on détecter des attaques inconnues sans disposer d'exemples de ces attaques pendant l'entraînement ?

- **Contexte :** un SOC veut savoir si l'apprentissage du comportement *normal* suffit à repérer des événements inconnus.
- **Dataset retenu :** **UNSW-NB15** (le sujet laissait le choix avec CICIDS2017).
- **Équipe :** 3 personnes (le sujet prévoit 4 : charge à répartir en conséquence). Chacun doit pouvoir expliquer n'importe quelle partie le jour de la soutenance.
- **Volume indicatif :** 21 h réparties en 7 phases.

---

## Vue d'ensemble

| Phase | Durée | Contenu | Livrable intermédiaire |
|---|---|---|---|
| 0 | — | Mise en place du dépôt et de l'environnement | Structure du repo, `requirements.txt` |
| 1 | 2 h | Problématique, choix et compréhension du dataset, EDA ciblée | Section EDA + hypothèses H1/H2/H3 formalisées |
| 2 | 2 h | Préparation des données, pipeline, splits, baseline | Pipeline sans fuite + résultats baseline |
| 3 | 3 h | Expérience 1 — comparaison de détecteurs | Tableau métriques + distributions des scores |
| 4 | 4 h | Expérience 2 — contamination | Courbes contamination vs Recall/FPR/F1 |
| 5 | 4 h | Expérience 3 — simulation zero-day | Comparaison Known/Unknown par famille |
| 6 | 3 h | Analyse approfondie, explicabilité, comparaison | Analyse FP/FN, SHAP/permutation, réponses Q1–Q4 |
| 7 | 3 h | Synthèse, rapport, slides, README, répétition | Tous les livrables finaux |

---

## Phase 0 — Mise en place

- [x] Structure du dépôt :
  ```
  data/            # brut (non versionné, voir .gitignore) + instructions de téléchargement
  notebooks/       # notebook principal (livrable)
  src/             # fonctions réutilisables (chargement, preprocessing, métriques, plots)
  results/         # tableaux CSV et figures générées
  report/          # rapport + slides
  README.md
  requirements.txt
  roadmap.md
  ```
- [x] Créer `.gitignore` (données brutes, checkpoints, `__pycache__`, `.ipynb_checkpoints`).
- [x] Environnement Python : `pandas`, `numpy`, `scikit-learn`, `matplotlib`/`seaborn`, `shap`, `jupyter`. (`.venv`, Python 3.14)
- [x] Figer les versions dans `requirements.txt` et définir une graine globale (`RANDOM_STATE = 42`).
- [ ] Répartir les responsabilités principales entre les 3 membres (sans cloisonner : revue croisée obligatoire).

---

## Phase 1 — Problématique, dataset et EDA ciblée (2 h)

### 1.1 Choix du dataset — ✅ UNSW-NB15
- [x] Dataset retenu : **UNSW-NB15**.
- [ ] Justifier le choix dans le rapport face à CICIDS2017 :
  - *UNSW-NB15* : colonne `attack_cat` (9 familles : Fuzzers, Analysis, Backdoor, DoS, Exploits, Generic, Reconnaissance, Shellcode, Worms), split train/test officiel, taille raisonnable.
  - *CICIDS2017* : très volumineux (fichiers par jour), problèmes connus (doublons, `Inf`/`NaN`, labels bruités).
- [ ] Utiliser les fichiers `UNSW_NB15_training-set.csv` / `UNSW_NB15_testing-set.csv` (version partitionnée, ~257k lignes) ; décider si on garde le split officiel ou si on recompose nos propres splits (nécessaire pour l'Exp. 3 zero-day).
- [ ] Attention aux familles à faible effectif (Worms, Shellcode, Analysis, Backdoor) : en tenir compte pour le choix des familles zero-day et l'interprétation des métriques par famille.

### 1.2 Compréhension du dataset
- [ ] Télécharger le dataset, noter la source et la version dans le README.
- [ ] Inventorier les features (numériques, catégorielles, identifiants à exclure : IP, ports, timestamps → risque de fuite).
- [ ] Lister les familles d'attaques et leurs effectifs.

### 1.3 EDA ciblée
- [ ] Répartition normal / attaque et par famille (déséquilibre).
- [ ] Valeurs manquantes, infinies, doublons, constantes.
- [ ] Distributions de quelques features clés normal vs attaque.
- [ ] Repérer les familles qui semblent proches du trafic normal (piste pour Q2).

### 1.4 Formalisation des hypothèses
- [ ] **H1** : les méthodes auront des compromis différents entre détection et faux positifs.
- [ ] **H2** : l'augmentation de la contamination réduira la capacité à distinguer normal et attaque.
- [ ] **H3** : certaines méthodes d'anomalies seront moins précises globalement mais plus utiles sur certaines familles inconnues.
- [ ] Pour chaque hypothèse : définir à l'avance la métrique et le critère qui la valideront ou l'infirmeront.

---

## Phase 2 — Préparation des données, pipeline et baseline (2 h)

### 2.1 Nettoyage
- [ ] Supprimer doublons, gérer `NaN`/`Inf`, retirer colonnes constantes et identifiants.
- [ ] Encoder les variables catégorielles `proto`, `service`, `state` (attention à la forte cardinalité de `proto`).
- [ ] Retirer `id`, `label` et `attack_cat` des features (labels uniquement pour l'évaluation et la construction des splits).

### 2.2 Stratégie de split (point critique)
- [ ] Définir **train / validation / test** clairement et les documenter.
- [ ] Train des détecteurs d'anomalies = **trafic normal uniquement** (sauf Exp. 2).
- [ ] Validation = normal + attaques connues → sert au choix des seuils et hyperparamètres.
- [ ] Test = jamais utilisé pour une décision. Toute exception doit être signalée et justifiée.
- [ ] Prévoir dès maintenant la mise à l'écart des familles « zero-day » pour l'Exp. 3.

### 2.3 Pipeline sans fuite
- [ ] `sklearn.Pipeline` : scaling / encodage / sélection de features **fit uniquement sur le train**.
- [ ] Sous-échantillonnage éventuel (LOF et OC-SVM ne passent pas à l'échelle) : le faire de façon reproductible et identique pour tous les modèles.

### 2.4 Métriques communes
- [ ] Fonction unique d'évaluation : Precision, Recall, F1, Macro-F1, **FPR**, PR-AUC (+ ROC-AUC en complément).
- [ ] Ne jamais conclure sur l'accuracy seule.
- [ ] Stratégie de seuil commune (ex. percentile des scores sur le normal de validation, ou FPR cible) pour comparer les modèles équitablement.

### 2.5 Baseline
- [ ] Baseline simple avant les modèles complexes, par ex. : z-score / distance à la moyenne du normal, ou seuil sur une feature, ou détecteur aléatoire.
- [ ] Enregistrer ses résultats dans `results/`.

---

## Phase 3 — Expérience 1 : comparaison de détecteurs d'anomalies (3 h)

**Question :** quels compromis détection / faux positifs offrent les différents détecteurs ?

- [ ] Entraîner sur le normal uniquement : **Isolation Forest**, **Local Outlier Factor** (`novelty=True`), **One-Class SVM** (ou justifier une alternative, ex. autoencodeur).
- [ ] Mêmes données, même preprocessing, même règle de seuil pour tous.
- [ ] Réglage léger des hyperparamètres sur la **validation** uniquement.
- [ ] Résultats attendus :
  - [ ] Tableau Recall / Precision / F1 / FPR (+ PR-AUC) par modèle, baseline incluse.
  - [ ] Distribution des anomaly scores normal vs attaque (histogrammes / KDE) par modèle.
  - [ ] Courbes Precision-Recall.
- [ ] Rédiger selon la structure imposée : question, hypothèse, protocole, résultats, analyse, interprétation cyber, limites.

---

## Phase 4 — Expérience 2 : contamination (4 h)

**Question :** que se passe-t-il quand le jeu « supposé normal » contient des attaques ?

- [ ] Construire des jeux d'entraînement avec **0 %, 1 %, 2 %, 5 %, 10 %** d'attaques injectées.
- [ ] Taille totale du train constante entre niveaux ; tirage reproductible (graine fixée).
- [ ] Idéalement plusieurs tirages par niveau (ex. 3–5 graines) pour obtenir moyenne ± écart-type.
- [ ] Réentraîner chaque modèle de l'Exp. 1, même jeu de test pour tous les niveaux.
- [ ] Résultats attendus :
  - [ ] Courbes contamination vs **Recall**, **FPR**, **F1** (une par modèle).
  - [ ] Évolution des distributions de scores.
- [ ] Analyser : quel modèle est le plus robuste ? À partir de quel taux la dégradation devient-elle critique ?
- [ ] Rédiger selon la structure imposée.

---

## Phase 5 — Expérience 3 : simulation zero-day (4 h)

**Question :** les détecteurs d'anomalies repèrent-ils mieux que le supervisé des familles jamais vues ?

- [ ] Choisir **plusieurs familles** à retirer totalement de l'entraînement (justifier le choix : familles variées, effectifs suffisants).
- [ ] Vérifier qu'**aucune** observation de ces familles n'apparaît en train ni en validation.
- [ ] Entraîner :
  - [ ] les détecteurs d'anomalies (normal uniquement) ;
  - [ ] un **classifieur supervisé** (ex. Random Forest / XGBoost) sur normal + familles **connues** seulement.
- [ ] Évaluer séparément sur attaques **Known** vs **Unknown**.
- [ ] Résultats attendus :
  - [ ] Tableau comparatif Known / Unknown par modèle.
  - [ ] **Recall par famille** (heatmap modèle × famille).
- [ ] Rédiger selon la structure imposée.

---

## Phase 6 — Analyse approfondie, explicabilité et comparaison (3 h)

### 6.1 Analyse des erreurs
- [ ] Faux positifs : quels flux normaux sont signalés ? Caractéristiques communes ?
- [ ] Faux négatifs : quelles familles passent inaperçues ? Pourquoi (proximité avec le normal) ?
- [ ] Matrices de confusion par modèle et par famille.

### 6.2 Explicabilité
- [ ] Au moins une méthode : **SHAP** (TreeExplainer pour Isolation Forest / supervisé), **permutation importance**, ou feature importance.
- [ ] Comparer les features qui pilotent les anomalies vs celles du supervisé.
- [ ] Ne pas présenter une corrélation comme une causalité.

### 6.3 Questions d'analyse obligatoires
- [ ] **Q1.** Une anomalie est-elle nécessairement une attaque ?
- [ ] **Q2.** Quelles attaques ressemblent trop au trafic normal ?
- [ ] **Q3.** Quel niveau de faux positifs serait acceptable dans un SOC ? (raisonner en alertes/jour à partir du FPR et du volume de trafic)
- [ ] **Q4.** Pourquoi cette expérience ne suffit-elle pas à prouver la détection de tous les zero-day ?

### 6.4 Bilan des hypothèses
- [ ] H1, H2, H3 : validée / partiellement validée / infirmée, chacune reliée à un résultat mesuré.
- [ ] Séparer explicitement : **observation expérimentale** / **interprétation ML** / **interprétation cybersécurité** / **limite**.

---

## Phase 7 — Synthèse, livrables et soutenance (3 h)

### Livrables
- [ ] **Notebook** Jupyter/Colab propre, exécutable de bout en bout (Restart & Run All), commenté.
- [ ] **Rapport** 10–15 pages hors annexes : question de recherche, hypothèses, protocole, résultats, analyse, limites.
- [ ] Section **« Utilisation de l'IA »** dans le rapport (courte, factuelle).
- [ ] **Présentation** 10–15 diapositives.
- [ ] **README** : téléchargement du dataset, installation, ordre d'exécution, versions des bibliothèques, graines.

### Soutenance (15 min + 5 min de questions)
- [ ] Répartir la parole entre les 3 membres.
- [ ] Répétition chronométrée.
- [ ] Chaque membre relit l'ensemble du code et des choix pour pouvoir répondre à toute question.
- [ ] Préparer les questions probables : choix du seuil, fuite de données, choix des familles zero-day, Q1–Q4.

---

## Points de vigilance (à relire avant chaque phase)

- ❌ Conclure sur l'accuracy seule.
- ❌ Scaling, feature selection ou rééchantillonnage sur tout le dataset **avant** le split.
- ❌ Présenter une corrélation comme une relation causale.
- ❌ Qualifier une attaque d'« inconnue » si sa famille a servi à l'entraînement.
- ❌ Choisir le meilleur modèle ou le seuil sur le jeu de test.
- ✅ Toute conclusion doit être reliée à un résultat mesuré.
- ✅ Graines fixées, versions documentées, conditions comparables entre modèles.
- ✅ Les résultats, figures et conclusions proviennent d'expériences réellement exécutées (pas d'affirmations générées par IA non vérifiées).

---

## Gabarit à appliquer pour chaque expérience

| Élément | Contenu |
|---|---|
| Question de recherche | Ce que l'expérience cherche à déterminer |
| Hypothèse | Résultat attendu **avant** exécution |
| Protocole | Données, split, modèles, paramètres contrôlés, métriques |
| Résultats | Tableaux et figures réellement obtenus |
| Analyse | Explication des observations, comparaison à l'hypothèse |
| Interprétation cyber | Conséquences dans un SOC réel |
| Limites | Ce que l'expérience ne permet pas de conclure |
