*** Settings ***
Documentation     Teste Técnico QA Sênior - Parte 3 (Back-end)
...               Suite de testes de API usando Fakerestapi (Books).
...               São cobertos cenários de criação, consulta, atualização,
...               deleção de ID inexistente e envio de payload inválido.
Library           RequestsLibrary
Library           Collections
Library           DateTime

Suite Setup       Create Books API Session
Suite Teardown    Delete All Sessions

*** Variables ***
${BASE_URL}       https://fakerestapi.azurewebsites.net/api/v1
${BOOK_ID}        0

*** Keywords ***
Create Books API Session
    Create Session    books    ${BASE_URL}

Generate Current ISO Date
    ${now}=    Get Current Date    result_format=%Y-%m-%dT%H:%M:%S.000Z
    RETURN     ${now}

Generate Valid Book Payload
    ${publishDate}=    Generate Current ISO Date
    &{payload}=        Create Dictionary
    ...    id=0
    ...    title=Test Automation Advanced
    ...    description=Book created via automated test
    ...    pageCount=450
    ...    excerpt=Automation Book
    ...    publishDate=${publishDate}
    RETURN    &{payload}

Generate Invalid Book Payload
    ${publishDate}=    Generate Current ISO Date
    &{payload}=        Create Dictionary
    ...    id=0
    ...    title=Invalid Book
    ...    description=Book with negative page count
    ...    pageCount=-5
    ...    excerpt=Automation Book
    ...    publishDate=${publishDate}
    RETURN    &{payload}

*** Test Cases ***
1. Criar novo book com sucesso via POST /Books
    [Documentation]    Cria um novo book com payload válido e valida o retorno.
    &{payload}=    Generate Valid Book Payload
    ${response}=   POST On Session    books    /Books    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    200

    ${body}=       To Json    ${response.content}
    Log To Console    \n[INFO] Resposta da criação: ${body}
    # A API não persiste o registro, mas ecoa os dados enviados.
    Should Be Equal As Strings     ${body['title']}         ${payload['title']}
    Should Be Equal As Strings     ${body['description']}   ${payload['description']}
    Should Be Equal As Integers    ${body['pageCount']}     ${payload['pageCount']}
    Set Suite Variable    ${BOOK_ID}    ${body['id']}

2. Validar book existente via GET /Books/1
    [Documentation]    Recupera um book existente (ID 1) e valida alguns campos.
    ${response}=   GET On Session    books    /Books/1
    Should Be Equal As Integers    ${response.status_code}    200

    ${body}=       To Json    ${response.content}
    Log To Console    \n[INFO] Book ID 1: ${body}
    Should Be Equal As Integers    ${body['id']}    1
    Should Not Be Empty            ${body['title']}
    Should Not Be Empty            ${body['description']}

3. Atualizar book existente via PUT /Books/1
    [Documentation]    Atualiza o título de um book existente usando PUT.
    ${get_resp}=   GET On Session    books    /Books/1
    Should Be Equal As Integers    ${get_resp.status_code}    200
    ${book}=       To Json    ${get_resp.content}

    ${new_title}=  Set Variable    Updated Title via PUT
    Set To Dictionary    ${book}    title=${new_title}

    ${put_resp}=   PUT On Session    books    /Books/1    json=${book}
    Should Be Equal As Integers    ${put_resp.status_code}    200
    ${body_put}=   To Json    ${put_resp.content}
    Log To Console    \n[INFO] Book atualizado: ${body_put}
    Should Be Equal As Strings    ${body_put['title']}    ${new_title}

4. Deletar ID inexistente deve retornar 404 (comportamento incorreto documentado)
    [Documentation]    A API deveria retornar 404, mas retorna 200 mesmo para IDs inexistentes.
    ${invalid_id}=    Set Variable    0
    ${response}=      DELETE On Session    books    /Books/${invalid_id}
    Log To Console    \n[INFO] DELETE /Books/${invalid_id} - Status: ${response.status_code}
    Run Keyword And Continue On Failure    Should Be Equal As Integers    ${response.status_code}    200
    IF    ${response.status_code} == 200
        Log To Console    \n[WARN] A API não valida corretamente a exclusão de ID inexistente.
    END

5. Criar book inválido (PageCount = -5) evidencia ausência de validação server-side
    [Documentation]    Envia um payload inválido e verifica comportamento atual da API.
    &{payload}=    Generate Invalid Book Payload
    ${response}=   POST On Session    books    /Books    json=${payload}
    Log To Console    \n[INFO] Resposta criação inválida: status=${response.status_code}, body=${response.content}
    Should Be Equal As Integers    ${response.status_code}    200
