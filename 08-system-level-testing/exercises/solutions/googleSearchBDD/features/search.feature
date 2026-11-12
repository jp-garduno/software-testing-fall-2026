Feature: Login
  Scenario: Valid login
    Given I am on the login page
    When I enter username "admin"
    And I enter password "password123"
    And I click login
    Then I see the dashboard