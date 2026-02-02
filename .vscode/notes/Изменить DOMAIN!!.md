# Изменить DOMAIN!!

dto - frozen=True
schemas - pydantic

API JSON → Schema (валидация) → Mapper → DTO → внутренние слои

Schema: внутреннее представление данных API (валидация, десериализация)

DTO: контракт с остальной системой (публичный интерфейс клиента)

Mapper: мост между schema и DTO

добавить в __init__ всё важное