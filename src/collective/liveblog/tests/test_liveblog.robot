*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open Test Browser
Test Teardown  Close All Browsers

*** Variables ***

${TITLE} =  My liveblog
${DESCRIPTION} =  A liveblog is a blog post which is intended to provide a rolling textual coverage of an ongoing event.
${TEXT} =  The body
${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator

    Go to homepage
    Create  ${TITLE}  ${DESCRIPTION}  ${TEXT}
    Update
    Delete

*** Keywords ***

Click Add Liveblog
    Open Add New Menu
    Click Link  css=a#liveblog
    Page Should Contain  Add Liveblog

Create
    [arguments]  ${title}  ${description}  ${text}

    Click Add Liveblog
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}

    Wait For Condition  return tinyMCE.activeEditor != null
    Execute Javascript  tinyMCE.activeEditor.setContent("<p>${text}</p>");

    Click Button  Save
    Page Should Contain  Item created
    Page Should Contain  ${title}
    Page Should Contain  ${description}
    Page Should Contain  ${text}

Update
    Click Link  link=Edit
    Click Button  Save
    Page Should Contain  Changes saved

Delete
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site
