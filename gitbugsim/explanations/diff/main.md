
[cyan]🧠 `git diff` – The Developer’s Magnifying Glass[/]

> `git diff` compares versions of files and shows the **exact changes** made between:
>
> * Working directory ↔ Staging area (Index)
> * Staging area ↔ Last commit (HEAD)
> * Commits, branches, files, or even binary files

---

[cyan]🛠️ Most Common Use Cases and Commands[/]

🔸 [yellow]`git diff`[/]

* ✅ Compares **working directory** vs **staging area**
* 📌 Use: Before `git add` to review unstaged edits

[green]💻 Example:[/]
  ```
  git diff
  ```

--- 

🔸 [yellow]`git diff --cached` or `--staged`[/]

* ✅ Compares **staged changes** vs **last commit (HEAD)**
* 📌 Use: Before `git commit` to review what you're committing

[green]💻 Example:[/]
  ```
  git diff --cached
  ```

---

🔸 [yellow]`git diff HEAD`[/]

* ✅ Compares **everything changed** (staged + unstaged) since last commit
* 📌 Use: To see full difference before making a commit or PR

[green]💻 Example:[/]
  ```
  git diff HEAD
  ```

---

🔸 [yellow]`git diff <file>`[/]

* ✅ Shows **unstaged changes** for a specific file
[green]💻 Example:[/]
  ```
  git diff main.py
  ```

---

🔸 [yellow]`git diff --cached <file>`[/]

* ✅ Shows **staged changes** for a specific file
[green]💻 Example:[/]
  ```
  git diff --cached app.js
  ```

---

🔸[yellow] `git diff <commit1> <commit2>`[/]

* ✅ Compares **any two commits**
* 📌 Use: Audit how code evolved
[green]💻 Example:[/]
  ```
  git diff a1b2c3d 98fgh456
  ```

---

🔸 [yellow]`git diff branch1 branch2`[/]

* ✅ Compares the **tips of two branches**
[green]💻 Example:[/]
  ```
  git diff main feature
  ```

---

🔸 [yellow]`git diff branch1...branch2`[/]

* ✅ Compares **branch2** with the **common ancestor** of both branches
* 📌 Use: PR diffs
[green]💻 Example:[/]
  ```
  git diff main...feature-login
  ```

---

🔸 [yellow]`git diff branch1 branch2 -- <file>`[/]

* ✅ Compares a specific file across two branches
[green]💻 Example:[/]
  ```
  git diff main feature -- login.js
  ```

---

🔸 [yellow]`git diff --color-words`[/]

* ✅ Shows **word-level diffs** (not full-line)
* 📌 Use: See precise edits (e.g., typos)

[green]💻 Example:[/]
  ```
  git diff --color-words
  ```

---

🔸 [yellow]`git diff | diff-highlight`[/]

* ✅ Highlights **sub-word** changes (requires setup)
* 📌 Use: Clean diff views in long lines

[green]💻 Example:[/]
  ```
  git diff | ./contrib/diff-highlight
  ```

---

[cyan]📂 Binary File Diffs[/]

🔸 `git diff` on PDFs, images, etc.

* ✅ Shows: `Binary files a/b differ` (not helpful by default)
* ✅ Setup textconv for readable diffs
* `.gitattributes`:

  ```
  *.pdf diff=pdfconv
  ```
* `.gitconfig`:

  ```ini
  [diff "pdfconv"]
  textconv=pdftohtml -stdout
  ```

---

[cyan]📘 Real Example Output Explained[/]

```diff
diff --git a/file2.py b/file2.py
new file mode 100644
index 0000000..ca098a5
--- /dev/null
+++ b/file2.py
@@ -0,0 +1 @@
+hey
\ No newline at end of file
```

---

[cyan]🔍 What Each Line Means:[/]

| Line                          | Meaning                           |
| ----------------------------- | --------------------------------- |
| `diff --git a/... b/...`      | File being compared (old vs new)  |
| `new file mode 100644`        | A new file added (non-executable) |
| `index 0000000..ca098a5`      | From nothing → to this version    |
| `--- /dev/null`               | Old file = nothing (new file)     |
| `+++ b/file2.py`              | New version of file               |
| `@@ -0,0 +1 @@`               | 1 line added at line 1            |
| `+hey`                        | Line added                        |
| `\ No newline at end of file` | Missing newline at file end       |

---

[cyan]🤔 What Happens If You Run `git diff --cached` with No Staged Files?[/]

* 🔇 Output will be **empty**
* ✅ Because there’s **nothing in the index to compare with HEAD**
* 💻 Use this instead to see unstaged changes:

  ```bash
  git diff
  ```

---

[cyan]🔁 Branch-Aware Behavior of `git diff --cached`[/]

* It **only compares staged changes** on the **current branch**
* **Does NOT compare with other branches**

Example:

```bash
git checkout feature
echo "test" >> app.js
git add app.js
git diff --cached
```

* ✅ Compares staged change in `feature` vs its own HEAD (not `main`)

---

[cyan]🆚 Comparing Branches with Staged Files[/]

| Use Case                                                              | Command                           |
| --------------------------------------------------------------------- | --------------------------------- |
| Compare 2 branches (entire diff)                                      | `git diff main feature`           |
| Compare a file across branches                                        | `git diff main feature -- app.js` |
| Compare staged change in current branch with another branch’s version | `git diff main --cached`          |

---

[magenta]🧠 Visual: Git Areas and How `diff` Works[/]

```
Working Dir  ←→  Staging Area  ←→  Last Commit
  (git diff)     (git diff --cached)   (HEAD)
       ↑                ↑                 ↑
     Unstaged        Staged            History
```

---

[cyan]🚀 Final Thought[/]

> `git diff` is **your safety net** before every commit, merge, or push.
> Use it constantly to understand, verify, and control what goes into your Git history.

