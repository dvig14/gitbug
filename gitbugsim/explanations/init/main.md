
🏁 git init : Initializes a new Git repository in the current or specified directory.

🧠 It creates a hidden folder called `.git`, which stores everything Git needs to track your project:
   • HEAD     :  Points to the current branch.
   • config   :  Repo-specific settings.
   • objects/ :  Stores actual content of commits, files, trees.
   • refs/    :  Pointers to branches, tags, remotes.
   • hooks/   :  Scripts triggered by Git events (e.g., pre-commit).
   • logs/    :  History of changes to references (like HEAD or branches). 
                 Creates only after the first commit or branch reference update.

💾 What this means:
• Every time you add, commit, or save your work with Git — the .git folder remembers it.
• Instead of saving full copies of files, it saves snapshots of changes (called commits).
• All changes are local until you push to a remote

👥 In team projects, Git (through .git) knows:
   ✓ Who made the change,
   ✓ When it happened,
   ✓ What exactly changed.
