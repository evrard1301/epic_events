Feature: As sales team member, I can manage customers.

   Scenario: Finding prospect.
     Given A prospect Alice.
     When I add the prospect.
     Then Alice has an account.
     And Alice is a prospect.

  Scenario: Create a contract with a prospect.
    Given A prospect Bob.
     When I add the prospect.
     And I create a contract.
     Then Bob is a prospect.

  Scenario: Signing a contract with a prospect.
    Given A prospect Carl.
    When I add the prospect.
    And I create a contract.
    And Carl sign the contract.
    Then Carl is a customer.
    Then Carl has 1 contract(s).

  Scenario: Signing a contract with a customer.
    Given A prospect Dan.
    When I add the prospect.
    And I create a contract.
    And Dan sign the contract.
    And I create a contract.
    And Dan sign the contract.
    Then Dan is a customer.
    Then Dan has 2 contract(s).


  Scenario: Update a customer phone number.
    Given A customer Dan.
    When I change customer phone to "000-111-222".
    Then The new phone is "000-111-222".
