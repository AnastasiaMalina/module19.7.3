from app.api import PetFriends
from app.settings import valid_email, valid_password, not_valid_email, not_valid_password
import os





pf = PetFriends()


# Позитивный тест
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""


# Отправляем запрос и сохраняем полусенный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
# Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

# Позитивный тест
def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого получаем api ключ и сохраняем в переменную auth_key. Далее испульзуя этот ключь
    запрвшиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# Позитивный тест
def test_add_new_pet_with_valid_data(name='Барсик', animal_type='кот',
                                     age='4', pet_photo='images/photo.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

# Получаем полный путь изображения и сохраняем в переменную pet_photo

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
# Запрашиваем ключ api и сохраняем в переменую auth_key

    _, auth_key = pf.get_api_key(valid_email, valid_password)

# Добавляем питомца

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

# Сверяем полученный ответ с ожидаемым результатом

    assert status == 200
    assert result['name'] == name

# Позитивный тест
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

# Получаем ключ auth_key и запрвшиваем список своих питомцев

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

# Проверяем список своих питомцев если он пустой, то добавляем нового и опять запрвшиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мурзик", "кот", "2", "images/photo2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

# Берем id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
# Запрашиваем список своих питомцев для проверки

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

# Приверяем что статус ответа равен 200 и в списке питомцев нет id удаленного питомца

    assert status == 200
    assert pet_id not in my_pets.values()

# Позитивный тест
def test_successful_update_self_pet_info(name='Гоша', animal_type='кот', age=6):
    """Проверяем возможность обновления информации о питомце"""

# Получаем ключм auth_key и список своих питомцев

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

# Если список не пустой, то пробойем обновить информацию о питомце

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)


# Проверяем что статус ответа 200 и имя питомца изменилось соответственно заданному

        assert status == 200
        assert result['name'] == name

    else:

# Если список питомцев пустой, то выкидываем исключение с текстом об отсутсвии питомцев

        raise Exception("You dont have any pets")

# Позитивный тест
def test_post_change_pet_foto(pet_photo='images/photo2.jpg'):
    """Проверяем добавление нового фото"""

# Получаем полный путь фоторафии питомца и сохраняем в перемнную pet_photo

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

# Запрашиваем ключ api и сохраняем в переменную auth_key и запрвшиваем список своих питомцев

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

# Проверяем список если он пустой,то добавляем нового питомца без фото,и опять запрвшиваем список своих питомцев

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Барсик", "кот", "4")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

# Берем id первого питомца из списка

    pet_id = my_pets['pets'][0]['id']

# Добавляем фото
    status, result = pf.post_change_pet_photo(auth_key, pet_id, pet_photo)
    print(result)
# Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] !=0

# Позитивный тест
def test_add_new_pet_without_photo_valid_data(name='Бобик', animal_type='собака',
                                              age='4'):
    """Проверяем что можно добавить питомца (без фото) с корректными данными"""
# Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

# Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

# Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Негативный тест

def test_get_api_key_for_not_valid_user_fail(email=not_valid_email, password=not_valid_password):
    """Негативный тест с проверкой невалидных значений not_valid_email, not_valid_password."""

# Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

# Сверяем полученные данные с нашими ожиданиями
    assert status == 403

# Негативный тест
def test_get_pet_with_not_valid_filter_fail(filter='Слон'):
    """Негативный тест. Проверяем что запрос с невалидным значением filter возвращает статус 500 и не выдает значений.
    Сначала получаем api ключ и сохраняем в переменную auth_key. Далее испульзуя этот ключ запрвшиваем список питомцев."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500

# Негативный тест
def test_add_new_pet_with_not_valid_age_fail(name='Мурзик', animal_type='кот',
                                                     age='слон', pet_photo='images/photo2.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными в раздел animal_type"""

# Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)


# Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

# Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

# Сверяем полученный ответ с ожидаемым результатом
    assert status ==200
    assert result['age'] == age

# Позитивный тест
def test_add_new_pet_with_big_valid_data(name='mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',
                                         animal_type='mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm', age='5677463882', pet_photo='images/photo.jpg'):
    """Добавление питомца с большим количеством символов в разделах name, animal_type, age"""

# Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

# Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

# Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
# Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['animal_type'] == animal_type
    assert result['name'] == name

# Позитивный тест
def test_add_new_pet_with_not_valid_data_fail(name='', animal_type='',
                                              age='', pet_photo='images/photo2.jpg'):
    """Проверяем создание питомца с пустыми значениями в разделах name, animal_type, age"""

# Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

# Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

# Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

# Сверяем полученный ответ с ожидаемым результатом

    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == animal_type
# Негативный тест
def test_post_change_pet_photo_fail(pet_photo='images/text.txt'):
    """Проверяем возможно ли отпраправить текстовый фаил вместо фотографии"""

# Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

# Запрашиваем ключ api и сохраняем в переменную auth_key и запрашиваем список своих питомцев

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

# Проверяем список если он пустой, то добавляем нового (без фото) и опять запрвшиваем список своих питомцев

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Пес", "кот", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
# Берем id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

# Добавляем фото
    status, result = pf.post_change_pet_photo(auth_key, pet_id, pet_photo)
    print(result)
# Сверяем полученный ответ с ожидаемым результатом
    assert status == 500


# Негативный тест
def test_successful_update_self_pet_info_numbers(name='111', animal_type='222', age='4'):
    """Проверяем возможность обновления значений name, animal_type о питомце только цифрами"""
# Получаем ключ api и список своих питомцев

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


# Если список не пустой, то обновляем такие данные как: name, animal_type, age

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name




    else:
# Если список пустой, то выкидываем исключение с текстом об отсутствии питомцев
        raise Exception("You dont have any pets")

# Позитивный тест
def test_add_new_pet_with_special_characters_data(name='!!!&%', animal_type='?|}', age='10', pet_photo='images/photo.jpg'):
    """Проверяем возможность добавить питомца с корректными данными спецсимволами в разделах name и animal_type"""

# Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

# Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
# Добавляем питомца
    status,result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
# Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
# Неготивный тест
def test_add_new_pet_without_photo_and_without_valid_data_fail(name='', animal_type='', age=''):
    """Проверяем создание питомца с пустыми значениями"""
# Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

# Добавляем питомца
    status, result  = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

# Сверяем полученный ответ с ожидаемым результатом
    assert status  == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age























