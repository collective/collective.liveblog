*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open Test Browser
Test Teardown  Close All Browsers

*** Variables ***

${TITLE} =  My liveblog
${DESCRIPTION} =  A liveblog is a blog post which is intended to provide a rolling textual coverage of an ongoing event.
${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator

    Go to homepage
    Create  ${TITLE}  ${DESCRIPTION}
    Update  ${TITLE}  ${DESCRIPTION}
    Delete

*** Keywords ***

Click Add Liveblog
    Open Add New Menu
    Click Link  css=a#liveblog
    Page Should Contain  Add Liveblog

Create
    [arguments]  ${title}  ${description}

    Click Add Liveblog
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Click Button  Save
    Page Should Contain  Item created

Update
    [arguments]  ${title}  ${description}

    Click Link  link=Edit
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Click Button  Save
    Page Should Contain  Changes saved

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site
