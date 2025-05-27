# Aperçu du Processus de Traitement (pipeline)

Le dossier `pipeline` contient des scripts conçus pour traiter et préparer les données pour l'analyse. Voici un aperçu des fichiers et de leurs objectifs :

## Description des Fichiers

1. **`conversion.py`**  
    Gère la conversion et la normalisation des données. Utilisez ce script pour transformer les données brutes en un format standardisé adapté à un traitement ultérieur.

2. **`labeling.py`**  
    Facilite l'étiquetage manuel des données. Après la normalisation, utilisez ce script pour attribuer des étiquettes aux données selon les besoins.

3. **`speed.py`**  
    Analyse et traite les données liées à la vitesse. Utilisez ce script pour calculer ou manipuler les métriques de vitesse.

4. **`speed_dist.py`**  
    Se concentre sur l'analyse de la distribution des vitesses. Utilisez ce script pour calculer et visualiser la distribution des données de vitesse.

## Flux de Travail

1. **Conversion et Normalisation des Données**  
    Commencez par `conversion.py` pour préparer vos données brutes.

2. **Étiquetage Manuel**  
    Utilisez `labeling.py` pour étiqueter les données normalisées.

3. **Analyse de la Vitesse**  
    Exécutez `speed.py` et `speed_dist.py` pour les calculs et visualisations liés à la vitesse.

Suivez cette séquence pour garantir un pipeline de traitement des données fluide.