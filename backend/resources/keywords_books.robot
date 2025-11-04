*** Settings ***
Library           RequestsLibrary
Library           JSONLibrary
Library           Collections
Library           DateTime
Library           String
Library           OperatingSystem

*** Variables ***
${BASE_URL}    https://jsonplaceholder.typicode.com
${BOOK_ID}        None

*** Keywords ***
Create Book Payload
    ${today}=     Get Current Date    result_format=%Y-%m-%dT%H:%M:%S
    ${title}=     Generate Random String    8
    ${payload}=   Create Dictionary
    ...           id=0
    ...           title=Test Automation Advanced ${title}
    ...           description=Book created via automated test
    ...           pageCount=450
    ...           excerpt=Automation Test
    ...           publishDate=${today}
    RETURN        ${payload}

Generate Invalid Payload
    ${payload}=   Create Dictionary
    ...           id=0
    ...           title=Invalid Book
    ...           description=Invalid Data
    ...           pageCount=-5
    ...           excerpt=Error
    ...           publishDate=2025-01-01T00:00:00
    RETURN        ${payload}

