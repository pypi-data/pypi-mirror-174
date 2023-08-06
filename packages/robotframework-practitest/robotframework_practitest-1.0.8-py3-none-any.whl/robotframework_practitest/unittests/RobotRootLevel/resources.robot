*** Variables ***
${TIMEOUT}  2
*** Keywords ***
Example KW 01
    [Documentation]  Stam01
    [Arguments]  @{args}
    sleep  ${TIMEOUT}
    log  KW: Example KW 01 ${args}


Example KW 02
    [Documentation]  Stam02
    sleep  ${TIMEOUT}  Long run
    log  KW: Example KW 02

Example KW 03
    [Arguments]  @{args}
    [Documentation]  Stam03
    sleep  ${TIMEOUT}
    log  KW: Fail example KW 03 - ${args}

Example KW 04
    [Documentation]  Stam04
    sleep  ${TIMEOUT}
    log  KW: Example KW 04

