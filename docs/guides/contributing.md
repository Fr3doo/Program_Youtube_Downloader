# Guide de contribution

Merci de votre intérêt pour **Program Youtube Downloader** ! Ce projet accepte les corrections de bogues et les améliorations mineures.

## Préparer l'environnement
1. Clonez votre fork du dépôt.
2. Créez un environnement virtuel (via `scripts/setup_env.sh` ou manuellement), puis installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
   ou bien installez le paquet localement :
   ```bash
   pip install .
   ```
3. Installez les dépendances de test si nécessaire (`pytubefix`, `pytube`, `colorama`).

## Lancer les tests
Avant toute soumission, assurez‑vous que la suite s'exécute sans erreur :
```bash
pytest
```
Les tests utilisent uniquement des objets factices et ne requièrent pas de connexion réseau.

## Proposer une modification
1. Créez une branche dans votre fork puis apportez vos changements.
2. Vérifiez le style et mettez à jour la documentation si besoin (voir `docs/`).
3. Exécutez `pytest` pour vérifier que tous les tests passent.
4. Ouvrez une *pull request* en décrivant clairement le problème résolu ou la fonctionnalité ajoutée.

Merci de consulter également `AGENTS.md` pour comprendre l'architecture du projet avant de proposer des évolutions plus importantes.
