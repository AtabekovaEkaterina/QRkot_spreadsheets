# QRkot_spreadseets


QRKot - это приложение для Благотворительного фонда поддержки котиков. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.


# Логика работы charity_project

В Фонде QRKot может быть открыто несколько целевых проектов. Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект. Каждый авторизованный пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.


# Google API
В приложение QRKot реализована возможность формирования отчёта в google-таблице. Отчет содержит в себе закрытые проекты, отсортированные по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.


# API проекта

**Основные эндпоинты проекта:**

- /charity_project/ — GET. Возвращающий список всех проектов (досупен всем пользователям);
- /charity_project/ — POST. Создаёт благотворительный проект (только для суперюзеров);
- /charity_project/{project_id} - DEL. Удаляет проект (только для суперюзеров);
- /charity_project/{project_id} - PATCH. Редактирование проекта (только для суперюзеров);
- /donation/ - GET. Возвращает список всех пожертвований (только для суперюзеров);
- /donation/ - POST. Сделать пожертвование (досупно всем пользователям);
- /donation/my - GET. Вернуть список пожертвований пользователя, выполняющего запрос(досупно всем пользователям);
- /auth/jwt/login - POST. Авторизация пользователя;
- /auth/jwt/logout - POST. Прекращение сеанса работы в качестве зарегистрированного пользователя;
- /auth/register - POST. Регистрация пользователя.


**Примеры запросов к API:**<br>

**GET** получение списка всех проектов<br>

`http://127.0.0.1:8000/charity_project/`
<details><summary>Response 200 удачное выполнение запроса</summary>
[<br>
  {<br>
    "name": "string",<br>
    "description": "string",<br>
    "full_amount": 0,<br>
    "id": 0,<br>
    "invested_amount": 0,<br>
    "fully_invested": true,<br>
    "create_date": "2023-10-18T15:45:55.893Z",<br>
    "close_date": "2023-10-18T15:45:55.893Z"<br>
  }<br>
]
</details>

**PATCH** обновление проекта<br>

`http://127.0.0.1:8000/charity_project/`
<details><summary>Request</summary>
{<br>
  "name": "string",<br>
  "description": "string",<br>
  "full_amount": 0<br>
}
</details>
<details><summary>Response 200 удачное выполнение запроса</summary>
{<br>
  "full_amount": 0,<br>
  "comment": "string",<br>
  "id": 0,<br>
  "create_date": "2023-10-18T15:49:17.846Z"<br>
}
</details>
<details><summary>Response 400 Bad Request</summary>
{<br>
  "detail": "Закрытый проект нельзя редактировать!"<br>
}
</details>


# Технологии

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)    Python 3.9<br>
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)     FastAPI<br>
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)    SQLite


# Инструкция по запуску

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AtabekovaEkaterina/cat_charity_fund.git
```

```
cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Обновить менеджер пакетов pip и установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

В корневой директории проекта создайть файл .env, с указанием в нем значений:

```
APP_TITLE=Кошачий благотворительный фонд
APP_DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
EMAIL=
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```

Подготовка для работы с google-таблицами:

1. Создайте гугл-аккаунт. Если он у вас уже есть, переходите в консоль облачной платформы Google Cloud Platform и авторизуйтесь https://console.cloud.google.com/projectselector2/home/dashboard;
2. Создайте проект в Google Cloud Platform (Create Project);
3. Подключить к проекту два API: Google Sheets API и Google Drive API (на плитке APIs нажмите Go to APIs overview -> Enabled APIs & services -> Enabled APIs and services -> Library);
4. Создать сервисный аккаунт (Credentials -> Create credentials -> Service account). Заполните форму для создания сервисного аккаунта, назначьте роль сервисному аккаунту - Editor. Введите адрес вашего личного аккаунта в поле Service account admins role;
5. Получите ключ и JSON-файл с данными сервисного аккаунта (Credentials -> нажмите на строчку с названием вашего сервисного аккаунта -> Keys –> Add Key –> Create New Key). Cохранитt файл, в котором будут собраны все необходимые данные для работы в приложении с подключёнными ранее API. Выберите формат JSON;
6. Перенесите данные из сохраненного файла в приложение QRkot в .env:

```
EMAIL=
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```

Запустить приложение:

```
uvicorn app.main:app
```


# Документация к проекту

- http://127.0.0.1:8000/docs - документация Swagger к проекту. Интерфейс документации Swagger позволит Вам: аутентифицироваться в приложении и создавать и отправлять запросы (вместо, например, Postman);
- http://127.0.0.1:8000/redoc - документация ReDoc.


# Константы проекта

MINIMUM_PASSWORD_LENGTH - минимальная длина пароля для пользователя<br>
TOKEN_VALIDITY_DURATION - срок действия токена в секундах<br>
LOG_FORMAT - вид, в котором сохраняются логи<br>
DT_FORMAT - формат времени для логов<br>
URL_FOR_GOOGLE_SHEETS - часть URL для просмотра сформированной google-таблицы


# Автор

Екатерина Атабекова
