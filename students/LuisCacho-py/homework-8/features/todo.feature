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

  Scenario: Unmark a completed todo
    Given I have a todo "Morning workout"
    When I mark the todo as complete
    And I unmark the completed todo
    Then the todo should be active
    And the active count should be 1

  Scenario: Edit an existing todo
    Given I have a todo "Draft presentation"
    When I edit the todo to "Final presentation"
    Then the todo should be "Final presentation"

  Scenario: Delete a todo
    Given I have a todo "Old task"
    When I delete the todo
    Then I should see 0 todos

  Scenario: Clear completed todos
    Given I have the following todos:
      | text          | completed |
      | Active item   | false     |
      | Finished item | true      |
    When I clear completed todos
    Then I should see 1 todo
    And the todo should be "Active item"

  Scenario Outline: Filter todos
    Given I have the following todos:
      | text      | completed |
      | Task 1    | false     |
      | Task 2    | true      |
      | Task 3    | false     |
    When I filter by "<filter>"
    Then I should see <count> todo(s)

    Examples:
      | filter     | count |
      | All        | 3     |
      | Active     | 2     |
      | Completed  | 1     |
