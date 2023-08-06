*** Settings ***
Documentation    Suite RobotFW to PT reporting
...   documentation example

Library  BuiltIn

Suite Setup  run keywords  Example KW 01  Arg1  Arg2
...         AND  Example KW 02
Suite Teardown  Example KW 04

Test Setup  run keywords  Example KW 01  Arg1  Arg2
...         AND  Example KW 02
Test Teardown  run keywords  Example KW 04
...         AND  set test message  ${TEST STATUS} - ${TEST NAME}

Resource  ../resources.robot

*** Test Cases ***
Test 1.1.1
    [Tags]  Smoke  Installation  Test-305  Custom-Test level-Smoke
    [Documentation]  Test 1.1.1 doc example
    ...   documentation example
    Example KW 02
    Example KW 03

Test 1.1.2
    [Tags]  Smoke  Test-305  Start
    [Documentation]  Test 1.1.2 doc example
    Example KW 02
    Example KW 03

*** Keywords ***
Provided precondition
    Setup system under test