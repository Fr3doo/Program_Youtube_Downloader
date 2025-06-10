# Guide : étendre la classe CLI

Ce tutoriel explique comment dériver `CLI` afin d'ajouter de nouvelles options ou d'adapter le menu interactif.
La fonction `main()` accepte un argument `cli_cls` pour instancier cette classe personnalisée.
Depuis la version 0.1.0, `CLI.__init__` prend aussi un paramètre `console`
implémentant `ConsoleIO`. Vous pouvez fournir un objet personnalisé pour
rediriger `input` et `print` durant les tests.

## Exemple minimal

```python
from program_youtube_downloader import cli_utils
from program_youtube_downloader.cli import CLI
from program_youtube_downloader.main import main

class MyCLI(CLI):
    def handle_hello_option(self) -> None:
        print("Bonjour !")

    def menu(self) -> None:
        while True:
            print("1 - Dire bonjour")
            print("0 - Quitter")
            choice = cli_utils.ask_numeric_value(0, 1)
            if choice == 0:
                self.handle_quit_option()
                break
            else:
                self.handle_hello_option()
```

```python
if __name__ == "__main__":
    main(cli_cls=MyCLI)
```

Ici `MyCLI` hérite de `CLI` pour ajouter une nouvelle entrée de menu. La fonction `main()` lancera cette classe et utilisera ses méthodes comme si elles faisaient partie de l'interface originale.
