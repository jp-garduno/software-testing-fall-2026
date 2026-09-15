# Homework 3 - Testing Report

## Introduction

For this homework, I made a simple calculator using Python. The main goal was to practice software testing and also use some tools that help keep the code organized and clean.

I decided to separate the calculator into different files instead of putting everything in one file. The project has three Python files inside the `src` folder: `calculator.py`, `operations.py` and `utils.py`.

The `operations.py` file has the different math operations, `utils.py` has some functions that help with the menu and user input, and `calculator.py` is the main part that connects everything together.

## Testing

For the tests, I used pytest. I created a file called `test_calculator.py` where I tested the different operations of the calculator.

I made tests for addition, subtraction, multiplication, division, power, modulo, average, finding the bigger number, finding the smaller number and percentage.

There are 10 tests in total. When I ran pytest, all the tests passed successfully:

`10 passed`

This was useful because instead of checking every operation manually, I could run all the tests at the same time and see if the results were correct.

For example, one of the tests checks that adding 5 and 3 gives 8. I also tested some of the other operations with simple numbers to make sure the calculator was giving the expected results.

## Code Quality

I also used pre-commit to check the code before making commits. The configuration includes different tools such as Black, isort and Pylint.

Black checks the format of the Python code, isort helps organize the imports, and Pylint checks for possible problems in the code.

At first, I had a problem with the Pylint configuration. Pylint was giving me an error because of the way one of the warning codes was configured. I had to check the configuration and make some changes until it worked correctly.

After fixing it, I ran the pre-commit checks again and everything passed. Black, isort and Pylint all passed, as well as the other file checks included in the configuration.

This part was a little annoying at first, but it was also useful because I learned that sometimes the problem is not necessarily in the code itself, but in the configuration of the tools being used.

## Project Organization

I tried to keep the project simple and easy to understand. The operations are in their own file, while the calculator and utility functions are separated.

I think this is better than having everything in one file because it makes it easier to find a specific function or make changes later.

The project also has a `requirements.txt` file with the dependencies needed for the project. I also created a README file with information about the calculator and instructions for running it and its tests.

## Git

I also used Git during the development of the homework. I made different commits as I worked on the project instead of putting all the changes into one commit.

I used conventional commit messages so it is easier to understand what each commit was about. For example, I used messages like `feat:` and `chore:` depending on the type of change.

Using Git this way helped me keep track of the different parts of the project and the changes I made.

## What I Learned

One of the main things I learned from this homework was that testing can make development easier. Even though this is a small calculator, having tests makes it easier to check that the operations are working correctly.

I also learned more about tools like pytest, Pylint, Black, isort and pre-commit. Before this project, I knew what some of these tools were for, but I had not used them all together in the same project.

I also learned that configuring these tools correctly is important. The Pylint problem was a good example of this because the code itself was not the main problem. The configuration needed to be fixed first.

## Conclusion

Overall, this homework helped me practice testing in a simple way. The calculator has 10 unit tests, and all of them are passing. The pre-commit checks are also working correctly.

I think the project is simple, but it helped me understand better why testing and code quality tools are useful. It also gave me more practice using Git and organizing a small Python project.

The part I found most useful was being able to run the tests and the pre-commit checks and know that the project was working correctly before continuing with the next steps.
