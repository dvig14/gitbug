🔀 Git Merge Conflicts: Why, How, When (With Examples)

---

[cyan]📌 What Is a Merge Conflict?[/]

A *merge conflict* occurs when Git *cannot automatically resolve differences* between two branches during a `git merge`.

---

[cyan]🤔 Why Do Merge Conflicts Happen?[/]

| Scenario                                                  | Description                                            |
| --------------------------------------------------------  | ------------------------------------------------------ |
| ✏️ *Same line edited in two branches*                    | Both branches changed the same line of the same file.  |
| ❌ *File deleted in one branch but modified in another*  | One branch deletes a file while the other modifies it. |
| 🔀 *Changes not committed before merge*                  | Local changes would be overwritten during merge.       |

---

[cyan]🕰️ When Do Merge Conflicts Occur?[/]

[yellow]✅ Common Merge Conflict Situations:[/]

1. *Collaborating on the same file*  
   Dev A and Dev B both edit `index.html` on different branches.

2. *Stale branches* 
   You've been working on a feature for days while `main` kept changing.

3. *Manual file edits + merge* 
   You modify a file and attempt to merge in another branch that also edited the file.

4. *Uncommitted changes*  
   You run `git merge` with local uncommitted edits that clash.

---

[cyan]⚠️ Merge Conflict Scenarios (Examples)[/]

[yellow]✅ Example 1: Same Line Edited[/]

# main branch
  echo "Hello world" > greet.txt
  git add .
  git commit -m "Initial commit"

# Create and switch to new branch
  git checkout -b feature-branch
  echo "Hello from feature branch" > greet.txt
  git commit -am "Feature edit"

# Go back to main
  git checkout main
  echo "Hello from main branch" > greet.txt
  git commit -am "Main edit"

# Try to merge
  git merge feature-branch

[red]❌ Git will output:[/]
CONFLICT (content): Merge conflict in greet.txt
Automatic merge failed; fix conflicts and then commit the result.


[yellow]✅ Example 2: File Deleted vs Modified[/]
# On main
  git rm config.json
  git commit -m "Removed config file"

# On feature branch
  echo "updated config" > config.json
  git commit -am "Edited config.json"

# Merge
  git checkout main
  git merge feature-branch

[red]❌ Git will say:[/]
CONFLICT (modify/delete): config.json deleted in main and modified in feature-branch.

---

[cyan]🧰 How to Handle Merge Conflicts (Step-by-Step)[/]

[yellow]✅ 1. Git Detects Conflict[/]
  git merge feature-branch
- Auto-merging greet.txt
- CONFLICT (content): Merge conflict in greet.txt

[yellow]✅ 2. Check Status[/]
  git status
- You have unmerged paths.
- both modified: greet.txt

[yellow]✅ 3. Examine the Conflict[/]
  cat greet.txt
<<<<<< HEAD
Hello from main branch
=======
Hello from feature branch
>>>>>> feature-branch

> This means:
- HEAD: your current branch (main)
- MERGING BRANCH: feature-branch

[yellow]✅ 4. Manually Edit and Resolve[/]
  Hello from main branch
  Hello from feature branch
- Save the file.

[yellow]✅ 5. Mark Conflict as Resolved[/]
  git add greet.txt
  git commit -m "Resolved merge conflict in greet.txt"
- ✅ Done!

---

[cyan]🔙 Abort the Merge (If You Want to Cancel)[/]
  git merge --abort
- 🔁 This restores your working directory and cancels the merge.

---

[cyan]🧪 Simulating a Merge Conflict (Demo)[/]

# 1
  mkdir git-merge-test && cd git-merge-test
  git init .
  echo "initial content" > file.txt
  git add .
  git commit -m "Initial commit"

# 2
  git checkout -b branch-A
  echo "change from branch A" > file.txt
  git commit -am "Edit from A"

# 3
  git checkout main
  echo "change from main" > file.txt
  git commit -am "Edit from main"

# 4
  git merge branch-A
  # CONFLICT!

---

[cyan]🛠 Helpful Commands for Merge Conflicts[/]

| Command                  | Purpose                             |
| ------------------------ | ----------------------------------- |
| `git status`             | Show conflicted files               |
| `git diff`               | View differences causing conflicts  |
| `git log --merge`        | Show conflicting commits            |
| `git merge --abort`      | Cancel the merge                    |
| `git reset --hard`       | Reset all changes (careful!)        |
| `git checkout -- <file>` | Revert file to last committed state |

---

[green]🧠 Pro Tips[/]
- ✅ Always commit or stash changes before merging.
- ✅ Work on feature branches to avoid polluting main.

---

[cyan]🔁 1. Stale Branches[/]

[yellow]❓ What is a Stale Branch?[/]
> A stale branch is a branch that has not been updated for a while, while the main branch (main or master) has had new commits added.
> This often happens when:
  - You started a feature branch (feature/login)
  - Meanwhile, your team added bug fixes, refactors, or features to main
  - When you try to merge your stale branch into main (or vice versa), conflicts may occur

[yellow]💥 Example: Conflict from a Stale Branch[/]

# Step 1: Initialize repo
  mkdir stale-demo && cd stale-demo
  git init
  echo "console.log('Hello')" > app.js
  git add .
  git commit -m "Initial commit"

# Step 2: Create feature branch
  git checkout -b feature-ui
  echo "console.log('Hello from feature-ui')" > app.js
  git commit -am "UI work in feature branch"

# Step 3: Go back to main and make other changes
  git checkout main
  echo "console.log('Hotfix on main')" > app.js
  git commit -am "Hotfix in main"

# Step 4: Merge feature branch into main
  git merge feature-ui

[red]❗ Output:[/]
Auto-merging app.js
CONFLICT (content): Merge conflict in app.js
Automatic merge failed; fix conflicts and then commit the result.

[green]✅ How to Resolve:[/]
# View conflict
  cat app.js

 <<<<<<< HEAD
 console.log('Hotfix on main')
 =======
 console.log('Hello from feature-ui')
 >>>>>>> feature-ui

[yellow]👉 Manually edit the file:[/]
 console.log('Hotfix on main')
 console.log('Hello from feature-ui')

# Then run:
  git add app.js
  git commit -m "Resolved conflict between main and feature-ui"

---

[cyan]📝 2. Uncommitted Changes During Merge[/]

[yellow]❓ What happens?[/]
> If you have uncommitted changes in your working directory and you try to run git merge, Git will refuse to start the merge if those changes overlap/conflict with the incoming changes.

[yellow]💥 Example: Merge Fails to Start Due to Uncommitted Changes[/]
# Create clean repo
  mkdir uncommitted-demo && cd uncommitted-demo
  git init
  echo "let x = 1;" > script.js
  git add .
  git commit -m "Initial commit"

# Create a feature branch
  git checkout -b feature-calc
  echo "let x = 2;" > script.js
  git commit -am "Updated x to 2 in feature"

# Switch back to main, make uncommitted change
  git checkout main
  echo "let x = 3;" > script.js  [red]# BUT DO NOT COMMIT![/]

# Try merging
  git merge feature-calc

[red]❌ Error:[/]
error: Entry 'script.js' not uptodate. Cannot merge.

[green]✅ How to Resolve:[/]
You have 3 options:

[yellow]✅ Option 1: Commit the changes first[/]
  git add script.js
  git commit -m "Local edit to x = 3"
  git merge feature-calc

[yellow]✅ Option 2: Stash the changes[/]
  git stash                                   [green]💡 To understand how stash works: git> explain stash[/]
  git merge feature-calc
  git stash pop

[yellow]✅ Option 3: Discard the changes (⚠️ permanent)[/]
  git checkout -- script.js
  git merge feature-calc







