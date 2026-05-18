# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

Règles spécifiques de la journée
• L’interprète à utiliser est python3.
• Chaque exercice est indépendant. Si parmi les features demandées, certaines ont
déjà été réalisées dans les exercices précédents, dupliquez- les dans l’exercice courant.
• Vous devez travailler dans une base de données postgresql nommée formationdjango
et créer un role nommé djangouser, dont le mot de passe est "secret", qui aura
tous les droits dessus.
• Votre dossier de rendu doit être un projet Django. Le nom du projet doit être celui
de la journée en cours.
• Nous allons utiliser le concept d’application de Django pour séparer les exercices :
Chaque exercice de la journée doit se trouver dans une application Django distincte
portant le nom de l’exercice correspondant et se trouvant à la racine du dossier de
rendu, .
• Le projet Django doit être configuré correctement afin de remplir les conditions
requises par les exercices. Aucune modification des configurations ne sera permise
en soutenance.
• Vous ne devrez rendre aucune migration avec votre travail.
• Dans chaque exercice dont le cartouche mentionne ORM, vous devez exploiter l’ORM
de Django. Aucune ligne de SQL ne doit être écrite.
• Dans chaque exercice dont le cartouche mentionne SQL, vous devez utiliser la librairie psycopg2 et effectuer toutes les requètes en SQL.
4
Formation Python-Django - 2 ORM
Voici un exemple de structure typique pour un rendu de l’étudiant krichard, concernant
la journée d42 et comprenant deux exercices :
|-- krichard
| |-- .
| |-- ..
| |-- .git
| |-- .gitignore
| |-- d42
| | |-- __init__.py
| | |-- settings.py
| | |-- urls.py
| | |-- wsgi.py
| |-- ex00
| | |-- admin.py
| | |-- apps.py
| | |-- forms.py
| | |-- __init__.py
| | |-- models.py
| | |-- tests.py
| | |-- urls.py
| | |-- views.py
| |-- ex01
| | |-- admin.py
| | |-- apps.py
| | |-- forms.py
| | |-- __init__.py
| | |-- models.py
| | |-- tests.py
| | |-- urls.py
| | |-- views.py
| |-- manage.py
.
Soyez malin : factorisez votre code et rendez le facile à réutiliser,
vous gagnerez du temps.



