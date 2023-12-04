# Тестовое DRF
## Описание

В папке `Testapp` хранится код основной части задания - бэкенд части приложения для создания и прохождения тестов. Приложение позволяет создать и отредактировать новый тест через обычный интерфейс админа Django (при локальной разработке - `http://127.0.0.1:8000/admin`). Остальное взаимодействие происходит через обычные REST запросы. Код написан с использованием `Django`, `Django Rest Framework`, `django-cors-headers`, `django-nested-admin`, а также в конце использовал `autopep8` и `isort` для форматирования кода.

Для пример в папке `client` хранится код клиентской части (без какой-либо стилизации), использующей запросы к API. Код был написан на `React`. Также тестировал API при помощи Postman. В браузере также есть возможность просматривать запросы (Browsable API в DRF), но для этого сперва нужно создать пользователя через Postman или админку.

## Запуск
### API
Создать и активировать виртуальную среду;
```sh
python3 -m venv env
source env/bin/activate
cd Testapp
python manage.py makemigrations
python manage.py migrate
```
Дальше необходимо создать суперпользователя:
```
python manage.py createsuperuser
```
После создания админа можно запустить сервер
```
python manage.py runserver
```
и по ссылке из терминала (вероятно, `http://127.0.0.1:8000`) будет доступен сервис. 
По ссылке `http://127.0.0.1:8000/admin` необходимо войти с данными админа. Оттуда можно создать тесты и просматривать результаты по моделям `Tests`, `Results`. В этом интерфейсе есть встроенная пагинация объектов (5 объектов на страницу) для обеих моделей. Тесты можно отфильтровать по полю "Публиковать ли", а также искать по названию теста. Результаты можно искать по названию соответствующего теста и имени пользователя, к которому относится результат. 
### Клиент
Для запуска клиентской части необходимо установить `node` и `npm`.
Из папки `client`:
```
npm ci
npm run start
```
Приложение будет доступно по ссылке `127.0.0.1:3000`.

## Использование
### Создание теста
Чтобы создать тест, необходимо в странице Tests создать новый тест. Далее ввести необходимое количество вопросов `n` и флаг публикации. После этого нажать на "Save and continue editing". Тогда появятся поля для создания вопросов (количество полей = `n`). Необходимо выбрать тип вопроса "Multichoice" или "Singlechoice" и ввести текст вопроса для каждого из `n` вопросов. Затем снова "Save and continue editing". После этого при клике на "Show" в секции `Choices` откроется блок с 2 опциями по умолчанию, дополнительные варианты ответа можно добавить вручную. При изменении моделей нужно сохранять с продолжением редактирования. По окончании создания можно нажать на кнопку "Save". Тест, относящиеся к нему вопросы с вариантами ответов будут сохранены.

### Использование API
В приложении реализована аутентификация по токену, токен создается автоматически при регистрации. При запросах на защищенные ресурсы (Test, Dashboard, Result) необходимо в headers.Authorization установить полученный токен.

|Path|значение|
|----|--------|
|/registration/register/|Создание нового пользователя|
|/registration/login/|Вход в аккаунт, получение токена|
|/|Список всех результатов и доступных для прохождения тестов конкретного пользователя|
|/test/<int:pk>/|Получение данных и отправка теста с id=pk|
|/test/<int:pk>/results/|Получение результатов по тесту конкретного пользователя|

### Ответы
Стоит отметить, что для корректной работы все ссылки запросов должны оканчиваться слэшем, например: `.../register/`( ~~`.../register`~~). Также большая часть ответов содержит, помимо статуса, дополнительную информацию в случае ошибки, но здесь описано только самое важное.

**401 ошибка** возникает при неавторизованных запросах на защищенные ресурсы. При её получении (или отсутствии токена в сессионном хранилище - для простоты реализации) в моем клиенте происходит перенаправление на страницу входа в аккаунт. 

#### Регистрация
Принимает POST-запрос. Валидации при регистрации почти нет. Необходим только объект с полями 'username' и 'password'. Проверка (например, повторение пароля) производится на стороне клиента.
- status=201 - успешно создан пользователь
- status=400 - уже есть такой пользователь (с таким же логином)

#### Вход в аккаунт
Принимает POST-запрос с username, password. Возвращает объект с данными.
- status=200 - успешный вход, объект содержит поле data['token'], содержащее токен (только строку, необходимо добавить "Token " при добавлении в хэдеры запроса)
- status=401 - неверный логин или пароль

#### Dashboard (path="/")
Принимает GET-запрос без body. Отображает все доступные для просмотра страницы результатов и открытых тестов. Если в базе есть тест, но он скрыт и не был пройден, пользователь не получит его в списке.

В случае успешного запроса поле "data" ответа содержит массив объектов вида: 
```
{
    "id": номер теста, в моем клиенте используется для перехода на конкретный тест/результат,
    "test_name": Название теста,
    "is_available": булево значение;
}
```
`is_available` используется для определения, доступен ли тест к прохождению. Для доступных тестов равен True, для тех, что уже были пройдены, False.

- status=200 - успешно получены данные
- status=401 - пользователь не авторизован

#### Тест
Принимает POST и GET запросы. GET запрос в случае успеха содержит поле data с полями `test_name`:String, `questions`:List, каждый вопрос представлен объектом вида:
```
{
    'question_text': Текст вопроса,
    'question_type': "MC" или "SC" для Multichoice и Singlechoice,
    'choices': [
        {
            'question': id вопроса в базе, нужен для дальнейшей отправки формы, 
            'choice_text': текст варианта
        },
        ...
    ]
}
```

POST запрос ожидает в качестве body объект, где ключ - это `question` (тот самый id вопроса), а значение - массив выбранных вариантов (choice_text)
```
{
    '1': ['Первый ответ'],
    '2': ['Правильный ответ', 'Неправильный ответ']
}
```
При успешном запросе создастся новый объект модели Result, а также будет отправлен ответ с полями `status` и `message`="Ответы отправлены".

- status=200 - успешный GET-запрос
- status=201 - успешный POST-запрос
- status=400 - некорректный запрос
- status=401 -  пользователь не авторизован
- status=404 - теста нет среди доступных к просмотру или отправки (даже в качестве результата)
- status=423 - тест уже был пройден (ошибка и POST, и GET)

#### Result
Поддерживает только GET-запрос без body. Результат не может быть изменен даже из админки. Содержит и отправляет 4 поля:
```
{
    'username': имя прошедшего пользователя,
    'test_name': название теста,
    'test_id': ключ к тесту, id пройденного теста,
    'result_string': текстовое поле, репрезентующее результат прохождения
}
```
`result_string=models.TextField()` формируется при получениие формы теста. Есть иные варианты сохранить результат, но для покрытия задачи посчитал достаточным.

- status=200 - успешно получен результат
- status=401 - пользователь не авторизован
- status=404 - нет результатов для данного теста