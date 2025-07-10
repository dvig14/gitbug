
[cyan]💾 What is `git commit`?[/]
• Saves a snapshot of your staged changes into the Git **local repository**
• Think of it like "saving your progress" (only includes changes you've staged using `git add`)

---

[cyan]🔁 Git workflow overview[/]
  🛠️ Edit files      → Working Directory
  📥 Stage with add  → Staging Area
  💾 Commit          → Local Repository
  🚀 Push            → Remote Repository (GitHub, etc.)

---

[cyan]🧩 Common commit commands[/]
| Command                  | What it Does                                             |
| ------------------------ | -------------------------------------------------------- |
| `git commit`             | Opens editor to write a commit message                   |
| `git commit -m "msg"`    | Commits with a short inline message                      |
| `git commit -a -m "msg"` | Automatically stages and commits all **tracked** changes | 
| `git commit --amend`     | **Modifies** the last commit (message or files)          | 

💡[yellow] You Can run `git> explain commit --amend`[/] 

[yellow]git commit -a[/] [magenta]only adds tracked files that are not staged.
It never replaces a file already in the staging area, even if it’s modified again.
So better do:
  [yellow]
    add file-name
    commit -m 'msg'
  [/]
[/]

---

[cyan]✍️  Writing Good Commit Messages[/]
• Start with a short summary (under 50 characters)
• Leave a blank line
• Then add detailed explanation (optional)
• Use present tense: “Add user auth” not “Added user auth”

📦 Example:

    fix: correct login redirect bug

    - Adjusted logic in login.js to redirect to dashboard
    - Fixed a typo in route name

---

🎯 What is an [yellow]Atomic Commit[/]?
• A single, focused change per commit (easy to test, debug, revert)

[red]🔻 Bad Commit:[/]
    "fixed login + added profile pic + removed payment bug"

[green]✅ Good Commits:[/]
    fix: correct login redirect
    feat: add profile picture upload
    fix: payment flow crash on mobile

[yellow]🛠️  TIP:[/] `git add -p`
• Lets you interactively stage changes piece by piece (chunk-by-chunk)

---

[cyan]👥 Why clean commits matter[/]
• Helps teammates review and understand changes
• Easier to debug issues and reduce merge conflicts
• Reduce merge conflicts (you can understand it in scenarios)

---

[cyan]🔄 How to amend last commit[/]
    # After fixing or editing something...
    git add file.py
    git commit --amend
    
• It Reopens your last commit to modify files or fix the message

[yellow]💡 TRY: Run `git> log` to see your commit history![/]