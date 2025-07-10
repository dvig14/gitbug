
➕ git add : Stage Changes for Commit
─────────────────────────────────────────────

[yellow]🧠 What it does:[/]
• `git add` moves changes from your working directory to the *staging area*.
• Think of it like saying: "Hey Git, I want to save this part next."
• It doesn't save anything yet — that's what `git commit` does.

💡 Git doesn't track your file edits automatically.
You must *add* them first before committing.

[yellow]📘 Why use `git add`?[/]
• Gives you control over *what* goes into your next commit.
• Helps you avoid accidentally committing unrelated changes.
• Useful when you've edited multiple files but want to commit only some of them now.

[yellow]🧠 What is the staging area?[/]
• It's a buffer — a middle zone between editing and committing.
• Lets you group your changes into focused, meaningful commits.


[yellow]📘 BASIC WORKFLOW[/]

   1️⃣  Edit files (working directory)
   2️⃣  Stage changes with `git add`
   3️⃣  Confirm what's staged with `git status`
   4️⃣  Save with `git commit`


[yellow]🛠️  Common `git add` commands:[/]
| Command             | Description                                 |
|---------------------|---------------------------------------------|
| `git add <file>`    | Stage a specific file                       |
| `git add <folder>/` | Stage all changes in a folder               |
| `git add .`         | Stage all tracked & new files in this dir   |
| `git add -A`        | Stage **all** changes (including deletions) |
| `git add -p`        | Interactive mode — choose changes by chunk  |   [green] You Can run `git> explain add -p`[/]


[yellow]🔍 Example:[/]
Say you fixed a bug and added a new feature in one go.
You can stage only the bug fix first with:
    
    git add bugfix.py

[yellow]💡 Try:[/] `git> status` to verify what's staged  
        `git> commit -m "commit_msg"` to save your staged changes/work.