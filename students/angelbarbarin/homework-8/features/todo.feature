Feature: Todo Management
  As a user
  I want to manage my todo list
  So that I can track my tasks

  Background:
    Given I am on the todo page

  Scenario: Add a new todo
    When I add a todo "Buy groceries"
    Then I should see 1 todo
    And the todo should be "Buy groceries"

  Scenario: Complete a todo
    Given I have a todo "Read book"
    When I mark the todo as complete
    Then the todo should be marked as done
    And the active count should be 0

  Scenario: Delete a todo
    Given I have a todo "Old task"
    When I delete the todo
    Then I should see 0 todos

  Scenario: Edit a todo
    Given I have a todo "Buy milk"
    When I change the todo to "Buy oat milk"
    Then the todo should be "Buy oat milk"

  Scenario: Leaving edit mode without changes keeps the text
    Given I have a todo "Buy milk"
    When I start editing the todo and click outside
    Then the todo should be "Buy milk"

  Scenario: Clear completed todos
    Given I have the following todos:
      | text   | completed |
      | Task 1 | true      |
      | Task 2 | false     |
      | Task 3 | true      |
    When I clear the completed todos
    Then I should see 1 todo
    And the todo should be "Task 2"

  Scenario Outline: Filter todos
    Given I have the following todos:
      | text   | completed |
      | Task 1 | false     |
      | Task 2 | true      |
      | Task 3 | false     |
    When I filter by "<filter>"
    Then I should see <count> todo(s)

    Examples:
      | filter    | count |
      | All       | 3     |
      | Active    | 2     |
      | Completed | 1     |
