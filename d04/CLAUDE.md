# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

Règles spécifiques de la journée
• Les routes relatives à une application doivent être définies dans un fichier urls.py
se trouvant dans le dossier de cette application.
• Tout formulaire (classe dérivée de django.forms.Form) doit se trouver dans le
fichier forms.py de l’application à laquelle il est rattaché.
• Chaque page affichée doit être correctement formatée (présence d’un doctype, de
couples de balises html, body, head), gestion correcte des caractères spéciaux, pas
d’affichage bizarre.
• Le serveur utilisé pour cette journée est le serveur de développement par défaut
de Django fourni avec l’utilitaire manage.py.
• Seules les URLs explicitement demandées doivent retourner une page sans erreur.
Ainsi, si seule /ex00 est demandée, /ex00foo doit retourner une erreur 404.
• Les URLs demandées doivent fonctionner avec et sans slash de fin. Ainsi, si /ex00
est demandée, /ex00 et /ex00/ doivent toutes les deux fonctionner.


