[yellow]🔍 `git log` – The Time Machine of Git[/]

> Hook:
> Want to know *who changed what*, *when*, and *why* in your code?
> `git log` is your personal *time machine* that shows the full *commit history* of your project.

---

[yellow]✅ What `git log` Does (Default Behavior)[/]

* 📜 Shows the **complete commit history** of your current branch.
* 📆 For **each commit**, it displays:

  * 🔑 Commit hash (unique ID)
  * 👤 Author (name & email)
  * 🕒 Date and time of commit
  * 📝 Commit message
* Commits are listed from **newest to oldest**.

---

🔧 Basic Command
[yellow]git log[/]

---

[yellow]📋 Sample Output Explained[/]

```
commit a1b2c3d4e5f6g7h8i9j0
Author: Diksha <diksha@example.com>
Date:   Mon Jul 1 14:35:10 2025 +0530

    Fix login button alignment issue

commit 987zyx654wvu321
Author: Diksha <diksha@example.com>
Date:   Sun Jun 30 10:12:45 2025 +0530

    Add user profile feature
```

[yellow]🔍 What Each Line Means:[/]

| Line            | Meaning                                      |
| --------------- | -------------------------------------------- |
| `commit <hash>` | Unique ID for the commit snapshot            |
| `Author`        | Who made the commit                          |
| `Date`          | When it was committed (+0530 = IST timezone) |
| Commit message  | A short description of the change            |

---

[yellow]🛠️ Where You Can Use `git log` (Real-World Use Cases)[/]

1. 🔍 Reviewing History
 - See what changes were made, by whom, and when.
 - Helps you understand project evolution over time.

2. 🧪 Debugging Code
 - When something breaks, use git log to find the last change.
 - Use it with git show <commit> to inspect exactly what changed.

3. 📅 Tracking Progress
 - See what features or fixes were added recently.
 - Useful for writing changelogs or status updates.

4. 🧠 Learning from Past Work
 - Understand why a change was made by reading commit messages.
 - Helps during code reviews and onboarding.

5. 🚀 Going Back in Time
 Get an older commit hash and use it to:
    git checkout <commit-hash>
 to view or test an old version of the project.

---

[yellow]🧠 How `git log` Helps You (Quick Table)[/]

| Situation                      | How `git log` helps                                          |
| ------------------------------ | ------------------------------------------------------------ |
| 🐛 Bug introduced recently     | Identify the last changes that may have caused it            |
| 🧼 Messy commit history        | Find and squash/reword bad commits                           |
| 👥 Collaborating with team     | See who made what changes                                    |
| 📝 Writing documentation       | Use commit messages to generate changelogs                   |
| 🧳 Navigating project versions | Get commit hashes for `checkout`, `revert`, or `cherry-pick` |



[yellow]🧪 Example Workflow[/]

git log

Output:
commit a1b2c3d...
    Fix login button alignment issue

You want to inspect it:
git show a1b2c3d

Result: You find exactly which line caused the issue ✅

 
[yellow]🧠 Bonus: Customize Your Git Log[/]

| Command                         | What it does                               |
| ------------------------------- | ------------------------------------------ |
| `git log --oneline`             | Short summary (1 line per commit)          |
| `git log --graph`               | ASCII tree view of branches and merges     |
| `git log --author="Diksha"`     | Filter commits by a specific author        |
| `git log --since="2 weeks ago"` | Show commits in a given time range         |
| `git log <filename>`            | Show history of changes to a specific file |



