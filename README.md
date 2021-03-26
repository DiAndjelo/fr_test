`git clone`

`cd fr_test`

`python -m venv venv`

`.\venv\Scripts\activate`

`pip install -r requirements.txt`

`python manage.py runserver`

api/interview/:
> interviews - список с опросами, поддерживает GET/POST,
> interviews/{id} - опрос с идентификатором {id}, поддерживает GET/PUT/DELETE

> то же самое для:
> questions, answers, choices, где questions - вопросы, choices - варианты ответов на вопросы, answers - ответы на вопросы пользователем

admin/:
> log/pass - admin/admin
> постарался сделать +- удобную админку с инлайнами для вопросов к опросу и выборами ответов для вопроса + ещё парочка удобных фич

фронт не писал
