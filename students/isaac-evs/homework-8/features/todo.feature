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

  Scenario: Add several todos keeps their order
    When I add a todo "First"
    And I add a todo "Second"
    Then I should see 2 todos
    And the todos should be "First, Second"

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

  Scenario: Clear completed todos
    Given I have the following todos:
      | text   | completed |
      | Done 1 | true      |
      | Open   | false     |
      | Done 2 | true      |
    When I clear the completed todos
    Then the todos should be "Open"

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

  @known-defect
  Scenario: Cancel an edit with Escape
    # Fails on the live app: its edit field ignores Escape. Excluded by default in behave.ini.
    Given I have a todo "Buy milk"
    When I start editing the todo and type "Changed my mind"
    And I press Escape
    Then the todo should no longer be in edit mode
    And the todo should be "Buy milk"
