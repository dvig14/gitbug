📚 Git Branches, `HEAD`, and Initial Commit Explained!

---
[cyan]📌 What is a Git Branch?[/]

* A *branch* is simply a pointer to a specific commit in Git.
* The default branch is usually `main` (used to be `master`).

   [yellow]git branch[/]         # Shows local branches

✅ After the first commit, this shows: * main

---

[cyan]📌 What is `HEAD` in Git?[/]

* `HEAD` is a special pointer that refers to the *current commit*.
* When you're on a branch, `HEAD` points to the *latest commit of that branch*.
* You can move `HEAD` to any commit using `git checkout`.

[yellow]📌 Examples:[/]

    git show HEAD         # Shows the current commit
    git log HEAD          # Log from current commit
    git diff HEAD         # Diff against current commit

❌ But if no commits exist, this will error:
[red]fatal:[/] ambiguous argument 'HEAD': unknown revision or path not in the working tree.

---

[cyan]📌 What Happens After `git init`[/]

* Git sets up a repository and creates a symbolic `HEAD` pointing to a default branch (`main` or `master`).
* However, the branch *doesn’t actually exist yet* until you commit.

[yellow]🧠 Git Limbo State:[/]

| Concept         | Exists? |
| --------------- | ------- |
| Branch (`main`) | ❌ No    |
| HEAD reference  | ✅ Yes   |
| Any commits     | ❌ No    |

---

[cyan]📌 Common Git Errors After Init[/]

[yellow]❌ `git show HEAD`[/]
   [red]fatal:[/] ambiguous argument 'HEAD': unknown revision or path not in the working tree.

[yellow]❌ `git branch`[/]
   No output!

[yellow]❌ `git checkout master`[/]
   [red]error:[/] pathspec 'master' did not match any file's known to git

---

[magenta]✅ How to Fix "HEAD unknown revision" Error[/]

[yellow]✅ Step 1: Make a Commit[/]

   echo "# Hello" > README.md
   git add README.md
   git commit -m "Initial commit"

[yellow]✅ Step 2: Try Commands Again[/]

   git log HEAD             # ✅ Works
   git branch               # ✅ Shows: * main
   git rev-parse HEAD       # ✅ Prints commit hash

---

[cyan]📌 How to Get the Current Branch Name[/]

Even if no commits exist yet, you can still *get the branch name*:

[yellow]✅ 1. Show branch name safely[/]
    git symbolic-ref --short HEAD     # Output: main (or master)

[green]✅ Works right after `git init`![/]

---

[cyan]📌 Why `git branch` Shows Nothing Initially[/]

After `git init`, Git shows:
    [yellow]On branch main[/]

But: [yellow]git branch[/]
Shows: nothing

🧠 Why?
> Because a branch isn't a real thing until it *points to a commit*.
> 🛠 Fix:
   [yellow]git commit -m "First commit"[/]       # Now git branch will show:[green] * main[/]

> Check which branch you’re on:
   [yellow]git symbolic-ref --short HEAD[/]      # Output: [green]main[/] or [green]master[/]

> To rename branch from main to master or vice-versa:
   [yellow]git branch -m master[/]

---

[cyan]📋 Summary Table[/]

| Problem                            | Cause                                  | Fix                                 |
| ---------------------------------- | -------------------------------------- | ----------------------------------- |
| `git show HEAD` error              | No commits → HEAD points nowhere       | Make an initial commit              |
| `git branch` shows nothing         | No commits → no actual branches        | Make an initial commit              |
| Can't get branch name              | `HEAD` is symbolic until commit        | Use `git symbolic-ref --short HEAD` |
| `fatal: ambiguous argument 'HEAD'` | HEAD is not resolved to a commit yet   | Commit something first              |

---

[cyan]💡 Bonus: Safe Commands for Early Git States[/]

| Command                           | Works Before First Commit? | Purpose                       |
| --------------------------------- | -------------------------- | ----------------------------- |
| `git symbolic-ref --short HEAD`   | ✅ Yes                      | Shows current branch name     |
| `git status`                      | ✅ Yes                      | Shows state of repo           |
| `git rev-parse --abbrev-ref HEAD` | ❌ No (throws error)        | Needs valid HEAD reference    |
| `git branch`                      | ❌ No                       | Needs a commit to show branch |

---

[cyan]🧠 Quick Example: First Commit Flow[/]

git init                          ->  Repo initialized
git status                        ->  On branch main (no commits yet)
git symbolic-ref --short HEAD     ->  main
git branch                        ->  No output

echo "hello" > a.txt
git add a.txt
git commit -m "Initial commit"

git branch                        ->  * main
git rev-parse HEAD                ->  commit-hash
git show HEAD                     ->  Shows commit details

