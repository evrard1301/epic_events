Feature: As management team member, I can administrate the system.

  Scenario: Adding a new management team member.
    Given A new member of the ManagementTeam.
    When I create its user account.
    Then The user can log in the CRM.
    And The user is in the group "ManagementTeam".


  Scenario: Adding a new support team member.
    Given A new member of the SupportTeam.
    When I create its user account.
    Then The user can log in the CRM.
    And The user is in the group "SupportTeam".

  Scenario: Adding a new sales team member.
    Given A new member of the SalesTeam.
    When I create its user account.
    Then The user can log in the CRM.
    And The user is in the group "SalesTeam".


  Scenario: Changing user team.
    Given A new member of the ManagementTeam.
    When I create its user account.
    And I change its group to SalesTeam.
    Then The user is in the group "SalesTeam".


