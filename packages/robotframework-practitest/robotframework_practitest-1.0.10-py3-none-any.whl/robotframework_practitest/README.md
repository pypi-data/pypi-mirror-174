# Introduction
Robot Framework plugin for report results to PractiTest

# Objectives
Plugin allow reporting as listener adding to robot execution
Based on.
* RobotFrameWork API  [Listener interface V3](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-version-3) 
* PractiTest API      [Version 2](https://www.practitest.com/api-v2/)

# Configuration

Following variables should be supplied to robot context on start.\
Possible ways:
- as CLI arguments
~~~
robot -v VAR_NAME:VAR_VALUE ... tests
~~~
- as yaml file loaded into robot files on root level in 
~~~
__init__.robot
*** Settings ***
Variables  practitest_info.yaml

~~~

## Variables
### Mandatory
~~~
PT_PROJECT_NAME:    Target project name in PractiTest
PT_USER_NAME:       User name
PT_USER_NAME_EMAIL: User email

PT_USER_TOKEN:     !!! Token expected from CLI only; don't put it in public sources !!!

PT_VERSION:         Version of execution
~~~
### Optionally
~~~
PT_EXTERNAL_RUN_ID: Optional suffix for TestSet name
PT_ENDPOINT:        PractiTest cloud URL (If omitted [https://api.practitest.com/api/v2/]  will be used) 
~~~

### Robot to PractiTest conversion policy & name conversion
RobotFW allow suites encapsulation by using folders and _.robot_ files.\
Following parameter define from which suite level start to create TestSets: _PT_TEST_SET_LEVEL_

__Examples:__
*`Robot tests example`*
~~~
RobotRootLevel
   __init__.robot
   Feature folder 1
       __init__.robot
       Sub feature 1.1
           __init__.robot
           Suite_file_1.1.1.robot
                Test 1.1.1.1
                Test 1.1.1.2
           Suite_file_1.1.2
                Test 1.1.2.3
                Test 1.1.2.4
       Sub feature 1.2
           __init__.robot
            Suite_file_1.2.1.robot
                Test 1.2.1.1
                Test 1.2.1.2
            Suite_file_1.2.2.robot
                Test 1.2.2.1
                Test 1.2.2.2
~~~

__*PT_TEST_SET_LEVEL: 0*__

TestSet will be created: 
>__Root level__


__*PT_TEST_SET_LEVEL: 1*__
 
TestSet will be created:
> __Root level/Feature folder 1__

__*PT_TEST_SET_LEVEL: 2*__
 
TestSet's will be created:
- __Root level/Feature folder 1/Sub feature 1.1__
-  __Root level/Feature folder 1/Sub feature 1.2__

__Notes:__ 
- _Each test from robot will be added in PractiTest if not exists by names as provided below_
- _All tests under related folder/sub folders/suites will be aggregated under correspond test set as well_

Test name will be followed by full path to test 

*Example:*

> Test 1.2.1.1 (Path: Root level/Feature folder 1/Sub feature 1.2/Suite_file_1.2.1/)

### Special variables
#### Mapping Robot Tags to PractiTest Custom field
PlugIn allow mapping of Robot test tags to PractiTest custom fields.

Firstly robot tag format shall be defined.

*Variable example:*
~~~
TAG_MAPPING:
  FIELD:
    prefix: Custom-
    delimiter: '-'  
  TEST:
    prefix: Test-
~~~
~~~
Robot test tag in format -> `Custom-Field name-001`.
Will be parsed as:       -> `prefix`-`field name`-`field value`, where '-' is delimiter
~~~
Will sync PractiTest TestLibrary field `Field name` with value `001`

#### Refer robot test to multimple tests in PractiTest
The difference between testing approaches between  PractiTests and RobotFW cause to reference needs to cover more then one test of PractiTest by one robot test

Robot test tag in format `Test-111` will add run instance of corresponding PractiTest test into target TestSet 



#### Map Robot variables to Test fields in PractiTest

~~~
PT_FIELDS_MAP:

  - id: &Status Status      <- Internal id and PractiTest field name
    variable: ROBOT_STATUS  <- Robot variable name
    default: Ready          <- Default value; Actually it make variable optional

  - id: &Severity           <- Internal id and PractiTest field name
    map: tags               <- Allow sync PractiTest test field from robot test tag
    default: Medium         <- Default value; Actually it make variable optional
    
    In some cases same field used be test and testset and have different behaiviour
    For this case can be define parameter with different id and same name
    
  - id: &Severity1          <- Internal id
    name: Severity          <- PractiTest field name
    default: Medium         <- Default value; There are actually way to setup permanent value

TEST_FIELDS:                <- Fields related to Test in PractiTest
  - *Status
  - *Severity

INSTANCE_FIELDS:            <- Fields related to Run instance in PractiTest (Not supported currently)
  - ''

TEST_SET_FIELDS:            <- Fields related to TestSet in PractiTest
  - *Severity1
  - *Status
~~~
