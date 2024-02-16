<h1 align="center">
    Learning API "Recipes"
</h1>
<p align="center">
    <em>Simple API development with FastAPI and Supabase as backend for an e-comerse of recipes</em>
</p>
<div align="center" style="display: flex; justify-content: center; gap: 0.5rem">
    <a href="https://opensource.org/licenses/MIT" target="_self">
        <img alt="GitHub License" src="https://img.shields.io/github/license/Jpena-code/recipes-api?color=yellow&label=License">
    </a>
    <a href="https://fastapi.tiangolo.com" target="_blank">
        <img alt="FastApi Page" src="https://img.shields.io/badge/FastAPI-project?style=flat&logo=FastAPI&label=API&style=plastic">
    </a>
    <a href="https://supabase.com" target="_blank">
        <img alt="Supabase page" src="https://img.shields.io/badge/Supabase-project?logo=Supabase&label=API&color=black">
    </a>
    <a>
        <img alt="Python Version from PEP 621 TOML" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FJPena-code%2Frecipes-api%2Fmain%2Fpyproject.toml&label=Python">
    </a>
</div>

<details open="open">
    <summary>Table of content</summary>

- [About](#about)
- [Installation](#installation)
  - [Prerequisite](#prerequisite)
  - [Environments](#environments)
- [API Reference](#api-reference)
    - [Login](#login)
    - [Get Records](#get-records)
    - [Get Record](#get-record)
    - [Post Tag or Category](#post-tag-or-category)
    - [Post Recipe](#post-recipe)
- [RoadMap](#roadmap)

</details>

----------
## About
API for a social media of recipes, this project is madded with the intent of learn about the well practices of software development at the process of develop an API, this is an approach of common basic requirements presents in the lifecycle of an API. The main technologies used in the project were [FastAPI](https://fastapi.tiangolo.com) as the framework for the HTTP server and the backend is deployed in a **Postgres SQL** server from the [Supabase](https://supabase.com) services.

## Installation

Feel free to download the report by cloning or forking the project environment.
```bash
git clone https://github.com/JPena-code/recipes-api.git .
cd recipes-api
```

### Prerequisite
The recommended method to run a local demo of this project is by using the python package manager [**Poetry**](https://python-poetry.org). Please refer to the official documentation of poetry to install it. After install you can run the follow command to install all dependencies.
```bash
poetry install --no-root --without=dev
```

### Environments
You can set the secret environments by exporting the variables in using the following shell commands or editing the [.env.example](/.env.example) file

```shell
export SUPABASE_URL=https://<reference-id>.supabase.co
# JWT secret
export SECRET=...
# JWT secrets keys
export ANON_KEY=...
export SERVICE_KEY=...
```

Finally to run the demo type the next command in your shell to have a local version of the API running
```bash
poetry run uvicorn --reload app.main:app
>> INFO:     Will watch for changes in these directories: ['/home/<user>/recipe-api']
>> INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
>> INFO:     Started reloader process [18035] using WatchFiles
>> INFO:     Started server process [18037]
>> INFO:     Waiting for application startup.
>> INFO:     Application startup complete.
```

## API Reference

This project is intended to replicated and implement the recommendations described by *FastAPI* when development a bigger application, starting by the folder structure bellow where the **CRUD** methods are condensed with the controllers classes. Additional and due to the lack of an **ORM** for *Supabase* to map the SQL tables with the application entities, the schemas were used as mappers from the *Supabase* API with the application logic.

```
└── 📁app
    └── 📁controller
        └── auth.py
        └── base.py
        └── category.py
        └── recipe.py
        └── tag.py
    └── 📁core
        └── 📁deps
            └── auth.py
            └── session.py
        └── events.py
        └── settings.py
    └── 📁db
        └── db.py
        └── 📁dummy
            └── data.json
    └── main.py
    └── 📁routers
        └── auth.py
        └── 📁v1
            └── category.py
            └── recipe.py
            └── tag.py
            └── user.py
    └── 📁schemas
        └── auth.py
        └── base.py
        └── categories.py
        └── recipes.py
        └── response.py
        └── tags.py
        └── user.py
    └── 📁utils
        └── _types.py
        └── 📁exceptions
            └── common.py
            └── handlers.py
```

The application consist of the following basic **endpoints** as a starting point to improve and evolve the application reach. Can access to the API documentation via the Docs Swagger provide by *FastAPI* following the [link](http://localbohs:8000/docs) when the app is up running

![Docs Swagger](/assets/docs_swagger.png)

#### Login
```http
  POST /api/login
  Content-Type: application/json
  Accept: application/json

  {
    "email": "string",
    "password": "string"
  }
```

#### Get Records

```http
  GET /api/v1.0/<tags,recipes,categories>
  Accept: application/json
  Authorization: Bearer api_key
```
| Parameter | Type     | Description                      |
| :-------- | :------- | :------------------------------- |
| `api_key` | `string` | **Required**. Your API key       |
| `page`    | `int`    | **Optional**. Page Query param   |
| `limit`   | `int`    | **Optional**. Length of the Page |

#### Get Record

```http
  GET /api/v1.0/<tags,recipes,categories>/${uuid}
  Accept: application/json
  Authorization: Bearer api_key
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `api_key` | `string` | **Required**. Your API key        |
| `uuid`    | `string` | **Required**. Id of item to fetch |

#### Post Tag or Category

```http
  POST /api/v1.0/<tags,recipes,categories>
  Accept: application/json
  Authorization: Bearer api_key
  Content-Type: application/json

  {
    "name": "string"
  }
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Post Recipe

```http
  POST /api/v1.0/<tags,recipes,categories>
  Accept: application/json
  Authorization: Bearer api_key
  Content-Type: multipart/form-data; boundary=--Limiter

  ----Limiter
  Content-Disposition: form-data; name=image; filename=image.png
  Content-Type: image/png,jpg,jpeg

  < image.png
  ----Limiter
  Content-Disposition: form-data; name=recipe_new
  Content-type: application/json

  {
    "title": "strings",
    "description": "string",
    "ingredients": "string",
    "instructions": "string",
    "tags": [
      "string"
    ],
    "category_id": "string"
  }
  ----Limiter--

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |


## RoadMap
- [x] **FastAPI** Backend
  - [x] **bigger** Application [Structure](https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=bigger)
  - [x] **auth** with supabase-py
  - [x] **CRUD** operations
- [ ] Supabase integration
  - [x] **auth** simple Supabase auth
  - [x] **CRUD** Supabase postgresql
  - [ ] **CRUD** Supabase storage
- [ ] Testing
  - [x] **simple Api** end-to-end testing
  - [ ] **CRUD** testing
- [ ] Deployment
- [ ] TODO
  - [ ] Use alias with pydantic
  - [x] Unified Logging
  - [ ] Standard errors **handlers** system
