# Homework 1 Reflection

One of the main challenges I faced during this assignment was understanding how feature branches, pull requests, and merge strategies affect the Git history. At first, I expected all commits from my feature branches to appear individually in my homework branch. However, after using the Squash and Merge option, I learned that GitHub combines the commits from a pull request into a single commit in the destination branch. This helped me better understand the difference between the history of a feature branch and the history of the main development branch.

The Git commands I found most useful were `git checkout -b` for creating branches, `git status` for checking my current changes, `git add` and `git commit` for recording work, and `git push` for sending my commits to GitHub. I also used `git pull` to keep my local branch synchronized after merging pull requests.

For this homework, I created the branches `feature/Luis-045/initial-structure`, `feature/Luis-045/add-styling`, and `feature/Luis-045/add-content`. Each branch focused on a specific part of the portfolio and was integrated through a pull request.

In a team project, I would use this workflow to separate features, avoid making changes directly to the main branch, and allow teammates to review changes before merging them. Clear branch names and meaningful commit messages would also make collaboration and debugging easier.