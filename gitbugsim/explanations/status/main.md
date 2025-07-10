
[cyan]🔍 What is `git status`?[/]
• Shows the current state of:
   - Your working directory (your edited files)
   - The staging area (files ready to commit)

---

[cyan]🧭 Why use it?[/]
• See which files:
   - Have been modified
   - Are staged for commit
   - Are untracked (new files)
• Helps avoid mistakes before committing
• Great for debugging and reviewing progress

---

[cyan]📦 What it tracks:[/]
| Type of File          | Status              | Shown as               |
| --------------------- | ------------------- | ---------------------- |
| Modified but unstaged | Not ready to commit | `modified:`            |
| Staged for commit     | Ready to commit     | `modified:`            |
| Untracked file        | Not being tracked   | `untracked:`           |
| Clean state           | No changes          | `working tree clean`   |

---

[yellow]🧪 EXAMPLE 1: Modified but Not Staged[/]
$ git status
On branch main  
Changes not staged for commit:  
  (use "git add <file>..." to stage)
    modified:   main.py

[green]✅ Explanation:[/]
• You edited `main.py` but haven't staged(added) it yet.
• Run `git add main.py` to stage it.


[yellow]🧪 EXAMPLE 2: File Staged for Commit[/]
$ git add main.py  
$ git status
On branch main  
Changes to be committed:  
  (use "git restore --staged <file>" to unstage)
    modified:   main.py

[green]✅ Explanation:[/]
• `main.py` is now staged and will be part of your next commit.


[yellow]🧪 EXAMPLE 3: Untracked File[/]
You created `notes.txt` but didn't stage it:
$ git status
On branch main  
Untracked files:  
  (use "git add <file>" to include in what will be committed)
    notes.txt

[green]✅ Explanation:[/]
• Git sees `notes.txt` but isn't tracking it.
• Run `git add notes.txt` to track it.


[yellow]🧪 EXAMPLE 4: Clean Working Tree[/]
After committing everything:
$ git status
On branch main  
nothing to commit, working tree clean

[green]✅ Explanation:[/]
• No changes pending — your repo is clean!

[yellow]🛠️  Useful Tips[/]
• Run `git status` often — it's your best friend!
• Combine it with:
   - `git add` to stage files
   - `git restore` to undo changes
   - `git diff` to see what's changed