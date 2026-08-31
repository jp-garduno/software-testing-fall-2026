# Reflection — Homework 1

I believe that having a good use knowledge on version control tools like git is fundamental for a software engineer or for anyone looking to pursue a development career. Using this tools in a regular basis is a non-negotiable in the job market. I personally did not get much from learning point of view by completing this task. If I'm 100% honest, I already use github everyday and am very familiar with the use-methodologies but I do understand that not everyone is familiarized with it so I see the utility and the purpose of this homework. Even tough AI coding tools are the ones that manage git  right now, it is important to know the funcamentals of everything so that you're not working blind.

## What challenges did you face?

I did not encounter any technical challenges, but since the page I did was intended to replace my work resume, I had quite a rough time redesigning my CV and updating it to complete the page's information. I am happy with the result and do believe that I'll be using this page as my new CV format, since I believe that it is a good way to make it stand-out from the rest, showing that I have some knowledge and interest in coding. 

## What Git commands did you find most useful?

Personally, the commands I use the most are commit's and branching. For new feature development and shipping I'm always making branches to work inside of them and actually I just saw a couple of days before, that Github just released a new function that allows you to stack many PR's into a single one, I still have to check it ouut but that will be extremely useful for shipping many features at a time.

## How will you apply this workflow in the team project?

Everyone will be in charge of it's own features and will be working on their separate branches off of the main one or a staging branch. There has to be someone charged with the role of reviewer so that everytime someone makes a pull request, he will be the one merging the changes into the main branch. Appart from that, of course every person in the team will have to work with a good methodology, not one-shoting everythin into one commit but dividing it into many different ones so that the reviewer job is easier and more effective. Also, this way and by also adding PR descriptions, aswell as screenshots (in my company, adding screenshots into PR's is mandatory for frontend features or UI changes) makes it easier to understand the purpose of the PR.

## Documentation of commit history and branching strategy

**Branches created for this homework:**

- `feat/pabloportillo1/homework-1` — submission branch in the course repo
- `feature/initial-structure` — HTML scaffold
- `feature/add-styling` — Kadu-Care-inspired styling
- `feature/add-content` — CV content, sections, links

**Commit convention:** Conventional Commits (`feat:`, `docs:`, `style:`, `fix:`, `refactor:`).

**Pull Requests:**

1. PR into `main` in the course repository with the `homework` label — this file's PR.

**Commit log (`git log --oneline` on this branch):**

```
docs(homework-1): document commit history in reflection
docs(homework-1): add reflection template for personal notes
docs(homework-1): add readme with git workflow documentation
feat(homework-1): add kadu-care inspired stylesheet
feat(homework-1): scaffold portfolio html with semantic structure
chore(homework-1): add gitignore for pabloportillo1 homework-1
```
