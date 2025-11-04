# 🧪 Teste Técnico QA – Selenium e API

Projeto dividido em **duas partes principais**:
1️⃣ **Frontend (Parte 2)** — automação de interface usando **Selenium + Pytest**.
2️⃣ **Backend (Parte 3)** — automação de API usando **Robot Framework + RequestsLibrary**.

---

## 📁 Estrutura do Projeto

```
Ambev/
│
├── backend ( arquivos de BE )
│  
└── frontend  ( arquivos de FE )
│ 
└── parte1analise ( parte de requisitos ) 
│  
└── testeBE.mp4  ( video rodando os testes )
│  
└── testefronte.mp4 ( video rodando os testes )

---

## 🚀 Parte 2 – Frontend (Selenium + Pytest)

### 🎯 Objetivo

Automatizar o preenchimento e envio do formulário disponível no site [DemoQA – Practice Form](https://demoqa.com/automation-practice-form).
O teste valida o fluxo de ponta a ponta, desde a abertura do site até a exibição do modal de confirmação.

### 🧰 Tecnologias utilizadas

* **Python 3.13+**
* **Selenium WebDriver**
* **Pytest**
* **WebDriverManager** (para gerenciamento automático do ChromeDriver)

### ⚙️ Execução local

1. Instalar as dependências:

   ```bash
   py -m pip install -r requirements.txt
   ```

2. Executar os testes:

   ```bash
   py -m pytest -v tests/test_practice_form_e2e.py
   ```

3. O teste abrirá o navegador, preencherá o formulário e exibirá o modal de sucesso.

### 📄 Resultados esperados

* O teste deve preencher todos os campos com sucesso.
* O modal final de confirmação deve aparecer com os dados enviados.
* Status final esperado:

  ```
  tests/test_practice_form_e2e.py::test_submit_practice_form_success PASSED
  ```

---

## ⚙️ Parte 3 – Backend (Robot Framework + RequestsLibrary)

### 🎯 Objetivo

Testar a API pública [Fakerestapi](https://fakerestapi.azurewebsites.net/api/v1/Books), validando os endpoints:

* **POST /Books**
* **GET /Books/{id}**
* **PUT /Books/{id}**
* **DELETE /Books/{id}**

### 🧰 Tecnologias utilizadas

* **Robot Framework**
* **RequestsLibrary**
* **Collections Library**
* **DateTime Library**

### ⚙️ Execução local

1. Instalar dependências:

   ```bash
   py -m pip install -r requirements.txt
   ```

2. Rodar a suíte de testes:

   ```bash
   py -m robot tests/books_api_tests.robot
   ```

3. Ao fim da execução, os seguintes arquivos serão gerados na pasta `backend/`:

   * `report.html`
   * `log.html`
   * `output.xml`

---

### 📄 Casos de Teste Implementados

| ID | Cenário                                | Método   | Endpoint   | Resultado Esperado                               |
| -- | -------------------------------------- | -------- | ---------- | ------------------------------------------------ |
| 1  | Criar novo book com sucesso            | `POST`   | `/Books`   | 200                                              |
| 2  | Validar book existente                 | `GET`    | `/Books/1` | 200                                              |
| 3  | Atualizar book existente               | `PUT`    | `/Books/1` | 200                                              |
| 4  | Deletar ID inexistente                 | `DELETE` | `/Books/0` | 404                                              |
| 5  | Criar book inválido (`pageCount = -5`) | `POST`   | `/Books`   | 200 (documentado ausência de validação)          |

---

### 🧩 Observações Importantes

* A API **não persiste dados** criados via `POST`.
* O endpoint `DELETE /Books/{id}` **retorna 200 mesmo para IDs inexistentes** — comportamento incorreto documentado nos testes.
* O teste 5 mostra que o backend **não valida corretamente valores negativos**, retornando 200 para `pageCount = -5`.

---

### ✅ Resultado esperado

```
Books Api Tests :: Teste Técnico QA Sênior - Parte 3 (Back-end)
==============================================================================
1. Criar novo book com sucesso via POST /Books               | PASS |
2. Validar book existente via GET /Books/1                   | PASS |
3. Atualizar book existente via PUT /Books/1                 | PASS |
4. Deletar ID inexistente deve retornar 404 (documentado)    | PASS |
5. Criar book inválido (PageCount = -5)...                   | PASS |
------------------------------------------------------------------------------
Books Api Tests                                              | PASS |
5 tests, 5 passed, 0 failed
==============================================================================
```

---

## 💡 Conclusões Técnicas

✅ **Boas práticas demonstradas:**

* Estrutura modular de testes com Pytest.
* Testes de API organizados no Robot Framework com separação por Keywords.
* Documentação e logs legíveis.

---

## Autor
**Rogério Lopes**



