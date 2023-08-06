*** Settings ***
Documentation    Suite RobotFW to PT reporting

Test Teardown  set test message  ${TEST STATUS} - ${TEST NAME}

Resource  ../resources.robot

*** Test Cases ***
Test 2.1.1
    [Tags]  Smoke  Test-115  Installation
    [Documentation]  Test 1.01 doc example
    Example KW 02
    Example KW 03

Test 2.1.2
    [Tags]  Smoke  Test-305  Start
    [Documentation]  Test 1.02 doc example
    Example KW 02
    Example KW 03

*** Keywords ***
