
[cyan]✅ Simulating a Real Git Commit Graph[/]

We’re building this commit structure:

```
[green]main:[/]     A──B──C [red]← HEAD[/]
             \\
[magenta]feature:[/]       D
```

Final `git log --graph --oneline --all`:

```
* <C> ([red]HEAD[/] -> [green]main[/]) Added login
* <B> Fixed bug in DB query
| * <D> ([magenta]feature/login[/]) Started login feature
|/
* <A> Initial commit
```

-----------------------------------------------------------------------------------------------------------------------

[yellow]📌 Step 1: Initial Commit (Commit A)[/]

- create file app.py and add content "print('Hello World')" and then stage n commit
    git> add app.py
    git> commit -m "Initial commit"

🧠 What It Does:
* Creates a new file `app.py` with a simple message.
* `git add` stages the file for committing.
* `git commit` saves the **first snapshot** (commit A).

💡 Key Concepts:
* This is your repo’s **root commit**.
* Git stores it as an **object** with a unique hash.
* The `main` branch now points to A.
* `HEAD` points to `main`, which points to A.

------------------------------------------------------------------------------------------------------------------------

[yellow]📌 Step 2: Commit B – Fix DB Bug[/]

- add content "def query(): return 'SELECT * FROM users'" to add.py and then stage n commit
    git> add app.py
    git> commit -m "Fixed bug in DB query"

🧠 What It Does:
* Adds a fake DB query to `app.py`.
* Creates the **second commit** in the chain (commit B).
* `main` → now points to B.
* `HEAD` follows main → now at B.

💡 Why It Matters:
* Git now tracks that `B` builds on top of `A`.

[magenta]🧱 Visual:[/]

A──B ← HEAD (on main)

------------------------------------------------------------------------------------------------------------------------

[yellow]📌 Step 3: Create `feature/login` Branch (off B)[/]

   git> checkout -b feature/login

🧠 What It Does:
* Creates a new branch called `feature/login`.
* Immediately switches you to it.
* `feature/login` starts from **commit B**.
* `HEAD` is now pointing to `feature/login`.

💡 Key Concepts:
* Git branches are just pointers.
* This branch still shares history with `main` up to commit B.

[magenta]🧱 Visual:[/]

main:     A──B
                 \
feature:          ← HEAD

------------------------------------------------------------------------------------------------------------------------

[yellow]📌 Step 4: Commit D – Work on Login Feature[/]

- add content "def login(): return True" to add.py and then stage n commit
    git> add app.py
    git> commit -m "Started login feature"

🧠 What It Does:
* Adds login-related code on `feature/login`.
* Git records this as commit D.
* `feature/login` → now points to D.
* `HEAD` is on D (via `feature/login`).

💡 Why It Matters:
* Now there is a **divergence** in the history:
  * `main` ends at B
  * `feature/login` continues with D

[magenta]🧱 Visual:[/]

main:     A──B
               \
feature:        D ← HEAD

------------------------------------------------------------------------------------------------------------------------

[yellow]📌 Step 5: Switch Back to `main`[/]

   git> checkout main

🧠 What It Does:
* Changes the current branch back to `main`.
* `HEAD` now points to commit B (latest on `main`).

💡 Key Concepts:
* You’ve not merged anything.
* Git just updates the working directory and pointer to match `main`.

[magenta]🧱 Visual:[/]

main:     A──B ← HEAD
               \
feature:        D

------------------------------------------------------------------------------------------------------------------------

[yellow]📌 Step 6: Commit C – Continue Work on `main`[/]

- add content "print('Login added')" to app.py and then stage n commit
    git> add app.py
    git> commit -m "Added login"

🧠 What It Does:
* Adds a separate line of login-related code (different from `feature/login`).
* Creates commit C on `main`.
* `main` now points to C.
* `HEAD` is now at C.

💡 Why It Matters:
* `main` and `feature/login` now have diverged histories.
* This is a true parallel development path.

[magenta]🧱 Final Visual:[/]

main:     A──B──C ← HEAD
               \
feature:        D

------------------------------------------------------------------------------------------------------------------------

[cyan]📊 Final Git Log Output:[/]

* <C_HASH> (HEAD -> main) Added login
* <B_HASH> Fixed bug in DB query
| * <D_HASH> (feature/login) Started login feature
|/
* <A_HASH> Initial commit

---

[cyan]Visual Flow Recap[/]

ASCII View:                        Git Log Output:
-----------------------          -------------------------------
main:     A──B──C ← HEAD         * C_HASH (HEAD → main)
               \\                * B_HASH
feature:        D                | * D_HASH (feature/login)
                                 |/
                                 * A_HASH Initial commit


