## Postes de travail

Le projet est mené depuis deux endroits qui ne se parlent que par git :

- **le téléphone**, via des sessions Claude Code dans le cloud (conteneur éphémère, sans Seamly2D) : lecture des photos, transcription, rangement, écriture ;
- **le PC**, qui a Seamly2D : tracés `.sm2d` et vérifications par export.

## Git : rebase, jamais de merge

L'historique reste linéaire : aucun commit de merge, ni local ni sur GitHub.

- Récupérer le travail de l'autre poste avec `git pull --rebase` (ou `git config pull.rebase true` une fois par clone).
- Une branche se met à jour par `git rebase origin/main`, pas par `git merge`.
- Une PR s'intègre à `main` avec **« Rebase and merge »** (méthode `rebase`), jamais « Create a merge commit ».
- Conflit pendant un rebase : le résoudre, `git rebase --continue`. Ne pas l'abandonner au profit d'un merge.
- Ne jamais forcer le push sur `main`. Sur une branche de travail, après un rebase, utiliser `git push --force-with-lease`.
