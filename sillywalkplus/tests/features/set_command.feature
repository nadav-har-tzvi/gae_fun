Feature: Set command
  Make sure that the set command actually sets and validates correctly and is up to requirements

  Scenario Outline: Set command with valid unique name-value pairs should result in a new entry in the datastore
    Given A blank datastore
    When Set command is invoked with <name> - <value>
    Then <name> should exist in the datastore
    And <name> value in the store should be <value>


    Examples:
    | name    | value    |
    | moshe   | 123      |
    | daphne  | fun      |
    | 443     | lipton   |

  Scenario Outline: Set command with invalid unique name-value pairs should do nothing
    Given A blank datastore
    When Set command is invoked with <name> - <value>
    Then <name> should not exist in the datastore

    Examples:
    | name    | value    |
    | @##@$@  | 123      |
    |  NULL   | fun      |
    | 443     | NULL     |

  Scenario Outline: Set command with non-unique valid name-value pairs should result in one appearance of each name
    Given A blank datastore
    When Set command is invoked with <name> - <value>
    Then <name> should exist in the datastore
    And <name> should appear only once

    Examples:
    | name    | value    |
    | moshe   | 123      |
    | moshe   | fun      |
    | 443     | lipton   |


    Scenario Outline: Set command with unique name-value pairs should result in each value's count being 1
      Given A blank datastore
      When Set command is invoked with <name> - <value>
      Then <value>'s count should be 1

      Examples:
      | name    | value    |
      | moshe   | 123      |
      | daphne  | fun      |
      | 443     | lipton   |


    Scenario: Set command with unique name but non unique value pairs should result in each value's count being N times it appeared
      Given A blank datastore
      When Set command is invoked with moshe - 123
      When Set command is invoked with daphne - 123
      Then 123's count should be 2


