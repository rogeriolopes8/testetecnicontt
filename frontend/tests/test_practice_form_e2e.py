from pathlib import Path

from pages.practice_form_page import PracticeFormPage


def test_submit_practice_form_success(driver):
    page = PracticeFormPage(driver)
    page.open()  # aqui ele já remove os anúncios internamente

    # Dados do enunciado
    first_name = "João"
    last_name = "da Silva"
    email = "joao@email.com"
    gender = "Male"
    mobile = "9999999999"
    day = 10
    month_index = 9  # Outubro (0-based)
    year = 1990
    subject = "Maths"
    hobbies = "Sports"
    address = "Rua dos Testes, 123"
    state = "NCR"
    city = "Delhi"

    # Caminho para a imagem de teste
    file_path = Path(__file__).resolve().parent.parent / "testdata" / "foto.jpg"

    # Preenchimento
    page.set_name(first_name, last_name)
    page.set_email(email)
    page.select_gender_male()
    page.set_mobile(mobile)
    page.set_birth_date(day, month_index, year)
    page.set_subject(subject)
    page.select_hobby_sports()
    page.upload_picture(str(file_path))
    page.set_current_address(address)
    page.select_state(state)
    page.select_city(city)

    page.submit()
    page.wait_for_modal()

    table = page.get_submission_table()

    # Validações
    assert table["Student Name"] == f"{first_name} {last_name}"
    assert table["Student Email"] == email
    assert table["Gender"] == gender
    assert table["Mobile"] == mobile
    assert "10 October,1990" in table["Date of Birth"]
    assert subject in table["Subjects"]
    assert hobbies in table["Hobbies"]
    assert address in table["Address"]
    assert table["State and City"] == f"{state} {city}"
