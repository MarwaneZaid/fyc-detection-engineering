# Detection Engineering pour un SOC

Cours FYC ESGI 2026-2027. Groupe : Victor Tassart, Marwane Zaid, Younès Hannour, Jacques-D'evaldo Tobossou. Mentor : Adam Rahmi.

GitHub est le seul endroit où l'avancement, les corrections et les décisions sont visibles. Le mentor suit le tableau entre les quatre séances. Il commente dans les pull requests. Il ne pousse pas de commits.

## Dossiers

| Dossier | Contenu |
|---|---|
| `videos/` | Scripts, sous-titres, liens des vidéos |
| `poly/` | Rapport écrit, 40 pages ± 2 |
| `rules/` | Règles Sigma ou SIEM |
| `exercises/` | 3 exercices Docker / GitHub et leurs corrigés |
| `exam/` | Sujet, corrigé, barème |
| `docker/` | Lab reproductible |

## Tableau

Les cartes sont les issues : une par vidéo, chapitre, exercice et pour l'examen. Le mentor ouvre [les issues](https://github.com/MarwaneZaid/fyc-detection-engineering/issues) ou [les jalons](https://github.com/MarwaneZaid/fyc-detection-engineering/milestones).

Une carte porte un seul label de statut. Le responsable le change quand l'étape change.

| Label | Sens |
|---|---|
| `statut: a-faire` | Pas commencé |
| `statut: en-cours` | En production |
| `statut: relu` | Relu par un autre membre |
| `statut: mentor` | En attente d'Adam Rahmi |
| `statut: valide` | Pull request approuvée |

Les jalons découpent l'année : séance 2 (environ 30 %), séance 3 (environ 50 %), séance 4, dépôt Moodle.

## Correction

1. Le responsable ouvre une pull request.
2. Un autre membre du groupe relit et demande les corrections de forme.
3. Le label passe à `statut: mentor`.
4. Le mentor commente sur le passage concerné.
5. La correction part sur la même branche. Le fil reste ouvert tant que ce n'est pas réglé.
6. L'approbation puis le merge sont la trace. Le label passe à `statut: valide`.

Une décision de séance (SIEM, nombre de vidéos, rôles) s'écrit dans une issue **Décision**, datée. Le rapport de séance pointe vers ces issues.

## Rythme

Deux points internes de 30 minutes par semaine. Chaque vendredi, une issue **État**. Les séances de 2 à 3 heures servent à la démo et aux choix, pas à découvrir l'état du projet.

## Inviter le mentor

Le dépôt est privé. Inviter Adam Rahmi avec le droit **Triage** : il lit, commente et approuve, sans écrire directement dans la branche principale.
