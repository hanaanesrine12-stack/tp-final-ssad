
## Fonctionnalités
### Parties 1 et 2 — Messagerie chiffrée

- Communication entre une entité A (émetteur) et une entité B (récepteur).
- Chiffrement et déchiffrement avec :
  - César ;
  - Hill ;
  - Playfair.
- Conservation du format du message lors du déchiffrement.
- Encodage des informations du canal sous la forme
  `code:sens:message_chiffre`.

### Partie 3 — Sécurité des mots de passe

- Création de comptes de démonstration.
- Validation de mots de passe selon les cas du sujet.
- Stockage avec sel et chiffrement.
- Vérification du mot de passe sans conserver le mot de passe en clair.
- Verrouillage temporaire après plusieurs échecs.
- Simulation d'attaques :
  - dictionnaire ;
  - force brute ;
  - dictionnaire puis force brute.

### Partie 4 — Intégrité des messages

- Calcul de l'empreinte SHA-256 du message chiffré.
- Vérification de l'empreinte par l'entité B.
- Détection de toute modification du message pendant le transport.
- Démonstration de l'effet avalanche : une seule modification produit une
  empreinte complètement différente.
- Simulation d'une falsification du message.

## Prérequis

- Python 3.10 ou version ultérieure.
- MySQL Server.
- Le connecteur Python MySQL.

Installation du connecteur :

```bash
python -m pip install mysql-connector-python
```

Tkinter est généralement inclus avec Python. Sous Linux, il peut être
nécessaire d'installer séparément le paquet `python3-tk`.

## Configuration de la base de données

L'application utilise une base MySQL nommée `crypto`. Créez-la avant le
lancement :

```sql
CREATE DATABASE crypto
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;
```

Les tables nécessaires sont créées automatiquement par l'application.

La connexion utilise les valeurs suivantes par défaut :

| Variable | Valeur par défaut |
|---|---|
| `CRYPTO_DB_HOST` | `127.0.0.1` |
| `CRYPTO_DB_PORT` | `3306` |
| `CRYPTO_DB_USER` | `root` |
| `CRYPTO_DB_PASSWORD` | vide |
| `CRYPTO_DB_NAME` | `crypto` |

Vous pouvez remplacer ces valeurs avec des variables d'environnement avant de
lancer l'application.

## Lancement

Depuis le dossier racine du projet :

```bash
python app.py
```

L'interface propose les onglets suivants :

1. **Messagerie** ;
2. **Mots de passe** ;
3. **Intégrité**.

## Tests

Pour exécuter les tests de chiffrement :

```bash
python -m unittest tests_partie2.py
```

Les tests supplémentaires disponibles dans le dépôt peuvent être lancés avec :

```bash
python -m unittest discover
```

## Organisation du projet

| Élément | Description |
|---|---|
| `app.py` | Point d'entrée de l'application graphique |
| `database.py` | Connexion MySQL, schéma et opérations de base |
| `partie2/` | Implémentation de César, Hill, Playfair et du canal |
| `partie2_interface.py` | Interface de messagerie |
| `passwords/` | Stockage, validation et attaques de mots de passe |
| `partie3_interface.py` | Interface de la partie 3 |
| `partie4/` | Hachage SHA-256 et vérification d'intégrité |
| `partie4_interface.py` | Interface de la partie 4 |
| `tests_partie2.py` | Tests des chiffrements de la partie 2 |

## Remarque de sécurité

Ce projet est une démonstration pédagogique. Le chiffrement de César et le
stockage par chiffrement César ne doivent pas être utilisés tels quels pour
protéger des données réelles. En production, il faut utiliser des algorithmes
modernes et dédiés, ainsi qu'un mécanisme d'authentification tel que HMAC pour
garantir l'authenticité des messages.
