# Code Review Guidelines

## 🎯 Purpose of Code Review

Code review is **NOT** about:

- ❌ Finding fault
- ❌ Showing you're smarter
- ❌ Gatekeeping

Code review **IS** about:

- ✅ Catching bugs before they reach production
- ✅ Sharing knowledge
- ✅ Maintaining code quality
- ✅ Learning from each other
- ✅ Ensuring consistency

---

## 👤 For Authors (Creating PRs)

### Before Creating PR

**Self-review checklist**:

- [ ] Code runs without errors
- [ ] All tests pass (unit, integration)
- [ ] Pre-commit hooks pass
- [ ] No debug statements (console.log, print)
- [ ] No commented-out code
- [ ] Documentation updated
- [ ] Clear PR description written

### Writing PR Description

Use the [PR template](../templates/pr-template.md). Include:

1. **What changed** - Brief summary
2. **Why it changed** - Problem being solved
3. **How to test** - Step-by-step instructions
4. **Screenshots** - For UI changes
5. **Related issues** - Closes #123

**Good PR description**:

```markdown
## What

Implements user authentication with JWT tokens

## Why

Needed to protect user-specific endpoints and personalize experience

## How to Test

1. POST to /api/auth/register with email/password
2. Verify user created in database
3. POST to /api/auth/login with credentials
4. Verify JWT token returned
5. Use token to access /api/users/profile

## Related

Closes #42, Related to #45
```

### PR Size

**Keep PRs small**:

- Small (< 200 lines): 15-30 min to review ✅
- Medium (200-400 lines): 30-60 min to review ⚠️
- Large (> 400 lines): > 60 min to review ❌

**If your PR is large**, consider:

- Breaking into multiple PRs
- Requesting early feedback on approach
- Adding more documentation

### Responding to Feedback

**Do**:

- ✅ Thank reviewers for feedback
- ✅ Ask clarifying questions
- ✅ Explain your reasoning politely
- ✅ Make requested changes promptly
- ✅ Mark conversations as resolved
- ✅ Re-request review after changes

**Don't**:

- ❌ Take feedback personally
- ❌ Argue defensively
- ❌ Ignore suggestions without discussion
- ❌ Make changes without acknowledging comments

**Example responses**:

```markdown
Good 😊: "Great catch! I'll add validation for that edge case."
Good 😊: "I chose this approach because X. Open to alternatives though!"
Bad 😞: "This works fine as is."
Bad 😞: "That's not important."
```

---

## 👥 For Reviewers

### Review Timeline

- **Within 24 hours**: Acknowledge the PR ("Will review today")
- **Within 48 hours**: Complete initial review
- **Within 24 hours**: Review changes after author updates

### What to Review

#### 1. Correctness (30%)

**Does the code work?**

- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] No obvious bugs
- [ ] Error handling present
- [ ] Tests cover the changes

**Example comments**:

```markdown
❌ "This is wrong"
✅ "This will fail when user is null. Consider adding a check: if (!user) return error;"
```

#### 2. Design (25%)

**Is the code well-structured?**

- [ ] Functions are single-purpose
- [ ] No code duplication
- [ ] Appropriate abstractions
- [ ] Follows project patterns
- [ ] No over-engineering

**Example comments**:

```markdown
❌ "Bad design"
✅ "This logic is duplicated in 3 places. Could we extract it to a helper function?"
```

#### 3. Readability (25%)

**Is the code easy to understand?**

- [ ] Clear variable/function names
- [ ] Commented where necessary
- [ ] No overly complex logic
- [ ] Consistent with codebase style

**Example comments**:

```markdown
❌ "This is confusing"
✅ "Could we rename 'x' to 'userCount' for clarity?"
```

#### 4. Testing (20%)

**Is the code well-tested?**

- [ ] Tests added for new functionality
- [ ] Edge cases tested
- [ ] Tests are clear and maintainable
- [ ] Coverage doesn't drop

**Example comments**:

```markdown
❌ "Add tests"
✅ "Could you add a test for when the cart is empty? I think line 45 might throw an error."
```

### How to Give Feedback

#### Use Review Types

- **Comment**: General feedback, questions, suggestions
- **Request Changes**: Blocking issues that must be fixed
- **Approve**: Ready to merge

#### Comment Structure

**Follow this pattern**:

```markdown
[Observation] - What you see
[Impact] - Why it matters
[Suggestion] - How to fix

Example:
"This query runs inside a loop (observation), which will cause N+1 queries as the list grows (impact). Consider fetching all items at once before the loop (suggestion)."
```

#### Use Clear Labels

Prefix comments to indicate priority:

- **[nit]** - Minor style issue, not blocking
- **[question]** - Asking for clarification
- **[suggestion]** - Nice-to-have improvement
- **[blocking]** - Must be fixed before merge
- **[praise]** - Highlight good work!

**Examples**:

```markdown
[nit] Extra whitespace here
[question] Why did we choose this approach over X?
[suggestion] This could be simplified with array.map()
[blocking] This will throw an error when user is undefined
[praise] Great test coverage! This will catch a lot of edge cases.
```

### Good vs Bad Comments

**Bad Comments** ❌:

```markdown
"This is wrong."
"Why did you do this?"
"No."
"Change this."
"I don't like this."
```

**Good Comments** ✅:

```markdown
"I think this will fail when X. Could we add a check?"
"Can you explain the reasoning behind this approach?"
"This works, but have you considered Y? It might be simpler."
"Could we extract this to a helper function for reusability?"
"I prefer approach X for consistency with file.py, but open to discussion."
```

### Balance Feedback

**Mix criticism with praise**:

```markdown
[praise] Love how you handled the error cases here!

[suggestion] For the email validation, could we use a regex pattern?
Would be more maintainable than the current if/else chain.

[question] Just curious - did you consider using a library for this?
What you built works great, just wondering about the trade-offs.

[praise] The test cases are excellent - really comprehensive!
```

---

## 🚦 Review Decision Guide

### ✅ Approve When

- No blocking issues
- Code works correctly
- Tests pass
- Minimal nits only
- Author has addressed feedback

### 💬 Comment (No Approval) When

- You have questions
- Want to suggest improvements
- Not ready to approve yet
- Waiting for discussion

### 🚫 Request Changes When

- Code doesn't work
- Tests are failing
- Security vulnerability
- Will break existing functionality
- Major design issues

**Note**: Only use "Request Changes" for serious issues. Use "Comment" for suggestions.

---

## 🎭 Review Scenarios

### Scenario 1: Everything Looks Good

```markdown
Looks great! ✅

[praise] Really clean implementation of the authentication flow.
[praise] Excellent test coverage - you covered all the edge cases I can think of.
[nit] One tiny thing: extra newline on line 45, but that's it.

Approving!
```

### Scenario 2: Minor Issues

```markdown
Nice work overall! Just a couple small things:

[suggestion] Could we rename `processData` to `validateUserInput`?
Would make it clearer what this function does.

[nit] Missing docstring on the `calculate` method.

[question] Why did we choose SHA256 over bcrypt for password hashing?
Bcrypt is generally recommended for passwords.

Not blocking, but would love your thoughts on these!
```

### Scenario 3: Blocking Issues

```markdown
Great start! A few issues we need to address before merging:

[blocking] The password is being logged on line 23. This is a security risk.
Need to remove that log statement.

[blocking] Tests are failing - looks like the user fixture is broken.

[blocking] This will crash when `user.email` is null.
We should add a null check: `if (user?.email)`

Once these are fixed, should be good to merge!
```

### Scenario 4: Design Discussion Needed

```markdown
Thanks for working on this! Before we proceed, I think we should discuss the approach.

[question] I see you're storing user sessions in memory. This will cause issues
when we scale to multiple servers. Have you considered using Redis or database sessions?

[suggestion] Instead of passing the entire user object around, could we just pass the user ID?
Would make testing easier and reduce coupling.

These might be bigger changes, so let's chat before you spend time on revisions.
Want to discuss in tomorrow's standup or async?
```

---

## 🔄 Review Workflow

### For Reviewers

1. **Read PR description** - Understand the what and why
2. **Check CI status** - Don't review if tests are failing
3. **Review code** - Focus on correctness, design, readability, tests
4. **Test locally** (for major changes) - Pull branch and test
5. **Leave feedback** - Use clear, kind comments
6. **Approve or request changes** - Be decisive

### For Authors

1. **Create PR** - Clear description, tests passing
2. **Request reviewers** - Tag appropriate team members
3. **Wait for feedback** - Give reviewers 48 hours
4. **Address feedback** - Make changes or discuss
5. **Respond to comments** - Thank reviewers, ask questions
6. **Re-request review** - After making changes
7. **Merge** - Once approved
8. **Delete branch** - Clean up after merge

---

## 📊 Code Review Checklist

### For Every PR

- [ ] Tests pass in CI
- [ ] Pre-commit hooks pass
- [ ] No merge conflicts
- [ ] Clear PR description
- [ ] Reasonable size (< 400 lines)

### Code Quality

- [ ] No hardcoded values (use config)
- [ ] No secrets in code (use env variables)
- [ ] Error handling present
- [ ] No debug statements
- [ ] No commented-out code
- [ ] Consistent with project style

### Testing

- [ ] Tests added for new code
- [ ] Edge cases covered
- [ ] Coverage maintained or improved
- [ ] Tests are clear and maintainable

### Documentation

- [ ] Code comments for complex logic
- [ ] README updated if needed
- [ ] API docs updated
- [ ] Docstrings/JSDoc present

---

## 💡 Pro Tips

### For Better Reviews

1. **Review in multiple passes**

   - Pass 1: High-level design and approach
   - Pass 2: Logic and correctness
   - Pass 3: Style and nits

2. **Use GitHub features**

   - Suggest changes (GitHub's "suggestion" feature)
   - Start a review (batch comments)
   - Use @ mentions for specific questions

3. **Set a timer**

   - Don't spend > 60 minutes on one review
   - If it's taking too long, PR might be too large

4. **Review your own PRs first**
   - Read through the diff before requesting review
   - Catch obvious issues yourself

### Common Traps to Avoid

❌ **Perfectionism**: Don't hold up good code for minor preferences  
❌ **Bikeshedding**: Don't debate trivial things (naming, formatting)  
❌ **Drive-by commenting**: Don't just point out problems without helping  
❌ **Scope creep**: Don't ask for unrelated features in review  
❌ **Review fatigue**: Don't review when tired or rushed

---

## 📚 Resources

- [Google Code Review Guidelines](https://google.github.io/eng-practices/review/)
- [How to Make Your Code Reviewer Fall in Love with You](https://mtlynch.io/code-review-love/)
- [The Art of Code Review](https://medium.com/@schrockn/the-art-of-code-review-e9e6b0f4b2e4)

---

**Remember**: Code review is about collaboration, not criticism. We're all learning together! 🤝
