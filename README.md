# catalog-service
Тестовое задание: REST API приложение для справочника Организаций, Зданий, Деятельности.

# Задача:
> Необходимо реализовать REST API приложения для справочника Организаций, Зданий, Деятельности.
* Организация - Представляет собой карточку организации в справочнике и должна содержать в себе следующую информацию:
  * Название
  * Номер телефона
  * Здание
  * Деятельность
* Здание - Содержит в себе как минимум информацию о конкретном здании, а именно:
  * Адрес
  * Географические координаты
* Деятельность - позволяет классифицировать род деятельности организаций в каталоге. Имеет название и может в древовидном виде вкладываться друг в друга. Пример возможного дерева деятельности:
```
- Еда
  - Мясная продукция
  - Молочная продукция
- Автомобили
  - Грузовые
  - Легковые
    - Запчасти
    - Аксесуары
```

## Функционал приложения:
> Взаимодействие с пользователем происходит посредством HTTP запросов к API серверу с использованием 
статического API ключа. Все ответы должны быть в формате JSON. Необходимо реализовать следующие методы:

- [x] Список всех организаций находящихся в конкретном здании
- [x] Список всех организаций, которые относятся к указанному виду деятельности
- [x] Список организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте.
- [x] Вывод информации об организации по её идентификатору
- [x] Искать организации по виду деятельности. Например, поиск по виду деятельности «Еда», которая находится на первом уровне дерева, и чтобы нашлись все организации, которые относятся к видам деятельности, лежащим внутри. Т.е. в результатах поиска должны отобразиться организации с видом деятельности Еда, Мясная продукция, Молочная продукция.
- [X] Поиск организации по названию
- [x] Ограничить уровень вложенности деятельностей 3 уровням

# Реализация

## 🐘 Схема базы данных:

![DB Schema](https://github.com/user-attachments/assets/309f07e7-d101-4315-be2f-f8623bbf8a16)

## 🐳 Запуск проекта в Docker:
> Перед запуском изменить `POSTGRES_HOST` в .env
```shell
# Postgres Environment Variables
POSTGRES_USERNAME="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_DB="catalog"
POSTGRES_HOST=postgres
POSTGRES_PORT="5432"
# FastAPI Environment Variables
SECRET_KEY="TEST-KEY"
```

```shell
docker compose -f docker-compose.yml --env-file ./src/.env up -d
```

## 📦 Заполнение БД тестовыми данными:
```shell
alembic upgrade head
python commands.py generate_data
# В docker
docker exec -i api python commands.py generate_data  
```

## 📍 Поиск организаций в заданном радиусе/прямоугольной области.

### 1. `search_organizations_by_search_point_and_radius`
> Мясной Дом - 4-й Добрынинский переулок, 1/9с1, Москва, 119049 - `55.724261, 37.617249`

![search_organizations_by_search_point_and_radius image](https://github.com/user-attachments/assets/5d80a1cb-21e9-46c5-a650-b42bcb783b3c)

#### Request
![Request search by radius](https://github.com/user-attachments/assets/2a546ff0-b522-4fac-a1da-628f1902d277)

#### Response
![Response search by radius](https://github.com/user-attachments/assets/7c3205f5-53f1-476a-a032-b28f15e7e649)

### 2. `search_organizations_by_rectangular_area`
> АвтоГруз - шоссе Энтузиастов, 50, Москва, 111123 - `55.759203, 37.758743`

![Search by area](https://github.com/user-attachments/assets/081c8005-1572-4b4b-b448-89a6d79a0e73)
#### Request

![Search by area request](https://github.com/user-attachments/assets/fd5cb578-4962-4c35-90b5-b7f76dda152d)

#### Response

![Search by area response](https://github.com/user-attachments/assets/6ef14c7f-80fe-45e8-8023-40e84019f12e)