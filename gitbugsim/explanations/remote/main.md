
[cyan]🚀 1. What Is an "Upstream" in Git?[/]

> An *upstream* is the remote branch your local branch tracks.

[yellow]🧭 It tells Git:[/]
* Where to *push* by default (`git push`)
* Where to *pull* from by default (`git pull`)

---

[cyan]✅ When Is Upstream Set Automatically?[/]

* [green]✅ *Yes*:[/] If you *clone* a repo → upstream is set automatically  
* [red]❌ *No*:[/] If you *create a branch locally* → you must set upstream manually

---

[cyan]📌 Common Commands[/]

| Command                                       | What It Does                                               |
| ------------------------------------------------------------------------------------------------------------ |
| `git push origin main`                        | Pushes to `origin/main`, but does NOT set upstream                   |
| `git push --set-upstream origin main`         | Pushes AND sets upstream — future `push` & `pull` work automatically |
| `git branch --set-upstream-to=origin/main main`| Only sets upstream, doesn'tpush                                     |


---

[cyan]🧪 Real Example: Created Branch Locally[/]

  git checkout -b main          # ✅ New local branch
  git remote add origin <url>   # ✅ Connect to remote
  git push origin main          # ✅ Pushes, but no upstream yet

  git pull                      # ❌ Fails!


[yellow]🔧 Fix it:[/]
  git push --set-upstream origin main


[yellow]Now:[/] git push    ✅
     git pull    ✅

---

[cyan]✅ Cloned Repos Behave Differently[/]
  git clone https://github.com/...
  cd demo
  git status


🧠 Git automatically links:
  [yellow]local `main` ↔ origin/main[/]


[yellow]So:[/] git push      ✅ works
    git pull      ✅ works

---

[cyan]🧠 Summary Table[/]

| Situation                      | `git push` | `git push origin main` | `--set-upstream` needed? | `git pull`   |
| ------------------------------ | ---------- | ---------------------- | ------------------------ | ----------   |
| Created branch locally         | ❌          | ✅                      | ✅                    | ❌          |
| Cloned a remote repo           | ✅          | ✅                      | ❌ already set        | ✅          |
| Ran `push --set-upstream` once | ✅          | ✅                      | No (now saved)         | ✅          |

---

[cyan]🔁 What Does git remote add Do?[/]
  [yellow]git remote add origin https://github.com/....[/]


| Part     | Purpose                                    |
| -------- | ------------------------------------------ |
| `origin` | Shortcut name (alias) for your remote repo |
| URL      | Actual location of the remote Git repo     |


Now you can use, instead of copying the full URL.
 [yellow]git push origin main[/]

---

[cyan]🔄 What Does git fetch Do?[/]
  [yellow]git fetch origin main[/]


| Action         | What It Does                                |
| -------------- | ------------------------------------------- |
| Fetches `main` | Downloads latest changes from `origin/main` |
| Doesn’t merge  | Your local `main` stays untouched           |


✅ Want to see what changed?
  [yellow]git diff main origin/main[/]

---

[cyan]🧨 What About git reset --hard origin/main?[/]
  [yellow]git reset --hard origin/main[/]


[cyan]🔥 This will:[/]
  🧹 Discard all local commits & changes
  🧭 Force local branch to match remote exactly


|[yellow] Use it when...[/]                           |
| --------------------------------------------------- |
| You messed up your local commits                    |
| You want to discard everything and sync with remote |

---

[red]🛑 WARNING: --hard Deletes Work![/]

| Command   | Safer Alternative              |
| --------- | ------------------------------ |
| `--soft`  | Keeps changes staged           |
| `--mixed` | Keeps changes unstaged         |
| `--hard`  | Deletes everything uncommitted |


