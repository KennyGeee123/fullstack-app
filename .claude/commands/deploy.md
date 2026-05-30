Generate a semantic commit message from the current git diff, commit all staged and unstaged changes, push to main, then monitor the GitHub Actions run until it completes.

Steps:
1. Run `git diff HEAD` and `git status` to see what changed
2. Write a concise semantic commit message (feat/fix/chore prefix) based on the actual diff
3. Run `git add -A && git commit -m "<message>"` 
4. Run `git push origin main`
5. Run `gh run list --repo KennyGeee123/fullstack-app --limit 1` to get the run ID
6. Run `gh run watch <run-id> --repo KennyGeee123/fullstack-app` to tail the pipeline
7. When complete, report the Vercel deployment URL from the run output
