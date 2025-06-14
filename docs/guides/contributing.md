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

Pour vérifier le comportement avec différentes options, vous pouvez exécuter la suite en modifiant les variables d'environnement :

```bash
PYDL_LOG_LEVEL=DEBUG pytest
PYDL_MAX_WORKERS=2 pytest
```

## Vérification du style et des types

Avant de proposer vos modifications, assurez-vous que le code respecte les
conventions du projet :

```bash
flake8
mypy program_youtube_downloader
```


# Module logging
Ce projet utilise le module `logging` de Python pour signaler l'état et les erreurs. Lors de l'ajout de nouveaux messages :

- Écrire les messages de journal en **français**.
- Utiliser des f-strings pour interpoler les variables.
- Rester concis et éviter les préfixes tels que `[ERREUR]`.

Exemple:
```python
logger.error(f"Echec du téléchargement : {exc}")
```

## Proposer une modification
1. Créez une branche dans votre fork puis apportez vos changements.
2. Vérifiez le style et mettez à jour la documentation si besoin (voir `docs/`).
3. Exécutez `pytest` pour vérifier que tous les tests passent.
4. Ouvrez une *pull request* en décrivant clairement le problème résolu ou la fonctionnalité ajoutée.

Merci de consulter également `AGENTS.md` pour comprendre l'architecture du projet avant de proposer des évolutions plus importantes.
