# Contribution guidelines

Ce projet utilise le module `logging` de Python pour signaler l'état et les erreurs. Lors de l'ajout de nouveaux messages :

- Écrire les messages de journal en **français**.
- Utiliser des f-strings pour interpoler les variables.
- Rester concis et éviter les préfixes tels que `[ERREUR]`.

Example:

```python
logger.error(f"Echec du téléchargement : {exc}")
```
