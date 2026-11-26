# TDD Reflection

I personally loved tdd. It was so easy to implement and every time I made a really small mistake I was able to spot it instantly where as withouth tests I would have spotted it debugging. It was't all perfect but this is what I think of it.

First of all, the biggest advantage of tdd is simplification. Any code, no matter how complex, gets easier to design with tdd. If you know what you want it to do. And if you can design the tests. Then you can figure out how to get your code from version A to B with ease. where A passes N tests and B passes N + 1. 

Another advantage when coding a complex software. Is taht the more complex the code, the more use to refactor you have. If the code is hard enough, the natural effect is you put all effort in refactoring. Writting tests is always easy, writting functionalities to pass one tests is too. You only find problems is you don't refactor. However if you refactor apropietly, writting complex logic resides only in the refactor phase. That is perfect because you don't break functionality and cant tests everytime for any mistakes. Combining complex logic with adding functionality can be a headheache but if you separate them it's leagues easier.

Likewise if TDD is good for complex software, easy software is inecessary and slow for easy software. But that brings us to the next advtange. If you work on a team, and need alot of tests. Even if it's a simple software, TDD becomes usefull. If the tests are needed, coding with TDD makes it so you spent 0 time debugging with no drawbacks. 

But then again, if you are not required to have tests. TDD can become a bit slow. One disadvantage of TDD is you need to design all tests perfectly. If you read 10% of requirements, write all tests which should be 10% of total, then code with tdd and continue reading requirements. You will find that the tests you wrote are no longer correct. You will need to fix them and fix code. For TDD to work you need requirements to be perfectly understood and tests to be perfectly made. Otherwise it won't be as fast as needed. Making TDD bad for simple softwares with not alot of team members. 

Finally TDD is bad with agents. AI does not refactor and can rewrite really easy. TDD avoids rewriting and relies on refactor. Those two make a horrible convo. 