# Reflection — Homework 5

**Student**: Isaac Vazquez (isaac-evs)

## What was most challenging about achieving high coverage?

Reaching the last few percent was mechanical, but getting there honestly was not. The service
tests mock the notification gateway, so after 80 tests the project was at 88% and the gateway
was almost untested. I had to mock one level lower, at the email and SMS clients. Dates were
the other trap: a fixed "now" in the tests collided with the real clock until I injected a clock
into the model and the service.

## How does white box testing differ from black box testing?

In Homework 4 I designed tests from the specification: partitions, boundaries, tables and states,
without caring how the code was written. Here I read the code and aimed tests at its branches,
exception handlers and guard clauses, and coverage told me exactly which ones I had missed.
Black box asks "does it do what was promised?"; white box asks "did I ever execute this path?"
Neither could replace the other. Coverage said nothing about the race in the duplicate-title check.

## Will I use code coverage in my future projects?

Yes, as a way to find untested code, with a branch report and a CI threshold around 80%. I
would not treat 100% as a target or as proof of quality. I would pair it with a mutation check;
a quick one on this project showed that the tests do fail when the code is wrong.
