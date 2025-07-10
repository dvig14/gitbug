
[cyan]📊 Git State Visualization — What This Means[/]

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📁 Working Directory        ┃ 📥 Staging Area            ┃   🗃 Commit History         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ (no untracked, unstaged…)   │ (no files staged…)          │                             │
│                             │                             │ aa0ac81: fixed              │
│                             │                             │ 02d40ba: add file           │
│                             │                             │ c8a920b: amend              │
└─────────────────────────────┴─────────────────────────────┴─────────────────────────────┘

[cyan]🧠 What Are These Sections?[/]

[yellow]1. 📁 Working Directory[/]

* This is your project folder on your computer.
* It contains real files (`.py`, `.html`, etc.).
* Git checks for **differences** between files here and the last committed version.
* Can include:

  * Untracked files = new files Git doesn’t know about.
  * Unstaged changes = modified files not yet marked for commit.
  * Clean = if there are no changes → like in your visual: *(no untracked, unstaged files)*

--------------------------------------------------------------------------------------------------------------------------

[green]2. 📥  Staging Area (Index)[/]

* Temporary area where you put files *before committing*.
* You use `git add` to move files here.
* If this is empty, it means you have nothing prepped for the next commit.

--------------------------------------------------------------------------------------------------------------------------

[blue]3. 🗃  Commit History[/]

* All your **past commits** (snapshots).
* They have:

  * A *commit hash* (e.g., `c8a920b`)
  * A *commit message* (e.g., `amend`, `add file`, `fixed`)
* Ordered from **most recent (top)** to **oldest (bottom)**

--------------------------------------------------------------------------------------------------------------------------

[yellow]📌 What Are "Untracked", "Unstaged", "Staged", and "Committed" Files?[/]

| State     | Meaning                                   | Command to Move to Next Stage |
| --------- | ----------------------------------------- | ----------------------------- |
| Untracked | New file not added to Git                 | `git add <file>`              |
| Unstaged  | File was tracked, but has unsaved changes | `git add <file>`              |
| Staged    | File is marked and ready to be committed  | `git commit -m "msg"`         |
| Committed | File changes are saved in Git history     | Already committed             |

--------------------------------------------------------------------------------------------------------------------------

✅ Let’s Recreate the Visual — Full Example

[yellow]📌 Step 1: Create and Commit File A (Commit: `c8a920b` - amend)[/]

- create file script.py and add content "print('v1')" , then run:
   git> add script.py
   git> commit -m "amend"

Now commit history:
   🗃  c8a920b: amend

--------------------------------------------------------------------------------------------------------------------------

[yellow]📌 Step 2: Add Another File and Commit (Commit: `02d40ba` - add file)[/]

- create file extra.py and add content "print('another file')" , then run:
   git> add extra.py
   git> commit -m "add file"

Now history becomes:
   🗃  02d40ba: add file
   🗃  c8a920b: amend

--------------------------------------------------------------------------------------------------------------------------

[yellow]📌 Step 3: Make a Fix (Commit: `aa0ac81` - fixed)[/]

- create file script.py and add content "# fixed bug" , then run:
   git> add script.py
   git> commit -m "fixed"

Now history is:
   🗃  aa0ac81: fixed
   🗃  02d40ba: add file
   🗃  c8a920b: amend

--------------------------------------------------------------------------------------------------------------------------

[yellow]✅ Check State with `git status`[/]

  git> status

Will *Git* output:

On branch main
nothing to commit, working tree clean


[cyan]🔎 That matches visual:[/]

* Working Dir: no untracked/unstaged files
* Staging Area: empty
* Commits: 3 entries → `fixed`, `add file`, `amend`

--------------------------------------------------------------------------------------------------------------------------

[cyan]🧠 Final Summary Table[/]

| Area              | Current State                            | Commands Involved        |
| ----------------- | ---------------------------------------- | ------------------------ |
| Working Directory | Clean (no modified/untracked files)      | `git status`, `git diff` |
| Staging Area      | Empty (nothing prepared for commit)      | `git add`, `git reset`   |
| Commit History    | 3 commits (`amend`, `add file`, `fixed`) | `git log --oneline`      |

--------------------------------------------------------------------------------------------------------------------------

[magenta]🧪 Bonus: Make It Dirty Again[/]

Want to see changes show up?

- Add "print('new stuff')" in already created file extra.py
  Now run:
           git> status

You’ll see:
* `extra.py` is *modified but not staged* 
* It’ll now appear in the 📁 Working Directory section as *unstaged*

Use this sequence, to add a 4th commit:

 git> add extra.py  
 git> commit -m "update extra"


