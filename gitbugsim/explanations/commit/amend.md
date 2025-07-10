
📝 git commit --amend : Modify Your Last Commit
────────────────────────────────────────────────

🔧 What it does:
• Replaces your **most recent commit** with a new one.
• You can:
   1. Edit the last **commit message**
   2. Add **more changes** to the same commit (i.e. Add more staged changes to the last commit.)

💡 Think of it like:
"Oops! I forgot something or made a typo — let me fix that last commit instead of making a new one."

---

🧰 Common Use Cases:

📌 1. Change the Commit Message
• You committed with a typo or unclear message.
• Just run:

    git commit --amend

→ You can rewrite the commit message.
→ Save and close to update it.

📌 2. Add Missed Changes to the Last Commit
• You forgot to stage a file or made a quick fix.

    echo "Add credits" >> README.md
    git add README.md
    git commit --amend

→ Now the commit includes both the original and new changes.

---

📘 Example:
Step-by-step:

    echo "console.log('Hi')" > script.js
    git add script.js
    git commit -m "Initial commit"

Oops! You forgot to add `index.html`:

    echo "<!DOCTYPE html>" > index.html
    git add index.html
    git commit --amend

✅ Now the commit contains both `script.js` and `index.html`

──────────────────────────────────────────────

[yellow]⚠️ Important Warning: Be Careful with Shared Commits![/]

If you already pushed the commit to a remote (e.g., GitHub), **amending it will rewrite history**.

👉 Example:
1. You run:
    git commit --amend
    git push origin main  ❌ (Fails!)

2. Git says: 
    ✖️ Rejected: tip of your current branch is behind

3. You'd need to **force-push**:
    git push --force

⚠️ This can overwrite your teammates work if they based changes on that commit.

---
    
🛑 Rule of Thumb:
• Only use `--amend` **before pushing**
• After pushing, prefer a new commit unless you're confident using `git push --force-with-lease`

[yellow]💡 Tip: Use `git log -1` to verify your amended commit![/]