
🎯 `git add -p` IN SIMPLE TERMS:
─────────────────────────────────────────────

- Imagine you wrote 4 lines in a notebook, but only want to share some.
- `git add -p` lets you choose which sentences to share (stage).

[yellow]🔸 Original notes.txt:[/]
  1. Buy milk
  2. Clean room
  3. Study Git

[yellow]🔸 You change it to:[/]
  - 1. Buy milk
  + 1. Buy oat milk
     2. Clean room
  - 3. Study Git
  + 3. Study Git in depth
  + 4. Learn Linux

---

[yellow]➡️  If you run:[/]
       git add notes.txt
    → All changes are staged.

---

[yellow]➡️  But if you run:[/]
    `git add -p` [Git shows you *hunks*]   

> Stage this hunk [y,n,q,a,d,s,e,?]?

    @@ -1,3 +1,3 @@
    -1. Buy milk
    +1. Buy oat milk

> You now decide:
    y - Yes, stage this change
    n - No, skip it

> Then it shows the next hunk:
    @@ -3,0 +4,2 @@
    +4. Learn Linux

> Only what you pick goes into the commit!

---

🎮 In Short: Like Picking Menu Items
🟢 Git: "Change 1: Add it?" → You say Yes.
🔴 Git: "Change 2: Add it?" → You say No.

ℹ️  To use `git add -p`, make sure the file is already 
    1. tracked (i.e., it's been added or committed at least once before) 
    2. modified (i.e., it has been modified after staging or committing)

--- 

[yellow]Try:[/]
    1. git add <filename>
    2. git commit -m "initial commit"
    3. Modify file
    4. Then use git add -p
