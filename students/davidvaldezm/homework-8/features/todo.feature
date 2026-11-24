Feature: Todo management
  As a user
  I want to manage my todo list
  So that I can track my tasks

  Background:
    Given I am on the todo page

  Scenario: Add a new todo
    When I add a todo "Buy groceries"
    Then I should see 1 todos
    And the visible tasks should be "Buy groceries"

  Scenario: Complete a todo
    Given I have a todo "Read book"
    When I mark the todo as complete
    Then the todo should be marked as done
    And the active count should be 0

  Scenario: Delete a todo
    Given I have a todo "Old task"
    When I delete the todo
    Then I should see 0 todos

  Scenario Outline: Filter todos
    Given I have the following todos:
      | text   | completed |
      | Task 1 | false     |
      | Task 2 | true      |
      | Task 3 | false     |
    When I filter by "<filter>"
    Then I should see <count> todos
    And the visible tasks should be "<tasks>"

    Examples:
      | filter    | count | tasks                  |
      | All       | 3     | Task 1, Task 2, Task 3 |
      | Active    | 2     | Task 1, Task 3         |
      | Completed | 1     | Task 2                |

  Scenario: Edit a task
    Given I have a todo "Draft"
    When I edit the todo to "Final"
    Then the visible tasks should be "Final"

  Scenario: Clear completed tasks
    Given I have the following todos:
      | text   | completed |
      | Keep   | false     |
      | Remove | true      |
    When I clear completed tasks
    Then the visible tasks should be "Keep"
    And the active count should be 1
