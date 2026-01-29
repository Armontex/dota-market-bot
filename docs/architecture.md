# Архитектура

## Содержание

- [Архитектура](#архитектура)
  - [Содержание](#содержание)
  - [MindMap](#mindmap)
  - [UseCases](#usecases)
    - [Frontend](#frontend)
      - [open-app-usecase](#open-app-usecase)
      - [auth-with-jwt-usecase](#auth-with-jwt-usecase)
      - [auth-with-telegram-usecase](#auth-with-telegram-usecase)
      - [change-profile-settings-usecase](#change-profile-settings-usecase)
      - [add-items-for-buy-usecase](#add-items-for-buy-usecase)
      - [remove-items-for-buy-usecase](#remove-items-for-buy-usecase)
      - [change-items-for-buy-usecase](#change-items-for-buy-usecase)
      - [add-items-for-sell-usecase](#add-items-for-sell-usecase)
      - [remove-items-for-sell-usecase](#remove-items-for-sell-usecase)
      - [change-items-for-sell-usecase](#change-items-for-sell-usecase)
      - [check-items-usecase](#check-items-usecase)
    - [Backend](#backend)
      - [buy-item-usecase](#buy-item-usecase)
      - [sell-item-usecase](#sell-item-usecase)
      - [notify-usecase](#notify-usecase)

## MindMap

```mermaid
%%{init: {"theme": "dark"}}%%
mindmap
  root((dota-market-bot))
    root((domain))
      auto-seller
      auto-buyer
    root((application))
        root((frontend))
          open-app-usecase
          root((auth))
            auth-with-jwt-usecase
            auth-with-telegram-usecase
          root((profile))
            change-profile-settings-usecase
          root((buy))
            add-items-for-buy-usecase
            remove-items-for-buy-usecase
            change-items-for-buy-usecase
          root((sell))
            add-items-for-sell-usecase
            remove-items-for-sell-usecase
            change-items-for-sell-usecase
          root((check))
            check-items-usecase
        root((backend))
          buy-item-usecase
          sell-item-usecase
          notify-usecase
        auto-trading-service
    root((infrastructure))
      frontend
      auth
      caddy-webserver
      notification-service
      root((clients))
        steam-client
        steamguard-client
        dota-market-client
      root((api))
        backend-api
      database
```

## UseCases

### Frontend

#### open-app-usecase

#### auth-with-jwt-usecase

*Совместно с [open-app-usecase](open-app-usecase)*

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant AuthWithJWTUseCase

    User->>Frontend: открывает<br>приложение
    Frontend->>Backend-api: GET /auth (с JWT если есть)
    Backend-api->>AuthWithJWTUseCase: execute(JWT)
    alt JWT действителен
      AuthWithJWTUseCase->>Backend-api: return Profile
      Backend-api->>Frontend: data
      Frontend->>User: Показать<br>открытое приложение
    else JWT нет/истёк
      AuthWithJWTUseCase->>Backend-api: return 401
      Backend-api->>Frontend: data
      Frontend->>User: Показать<br>форму авторизации
    end
```

#### auth-with-telegram-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant AuthWithTelegramUseCase

    User->>Frontend: Открывает страницу<br>регистрациии и нажимает<br>"Войти через Telegram"
    User->>Frontend: Авторизовывается<br>через Telegram
    Frontend->>Backend-api: POST /auth/social/telegram
    Backend-api->>AuthWithTelegramUseCase: execute(data)
    alt Авторизация
      AuthWithTelegramUseCase->>Backend-api: return Profile + JWT
      Backend-api->>Frontend: data
      Frontend->>User: Показать<br>открытое приложение
    else Регистрация
      AuthWithTelegramUseCase->>Backend-api: return Profile<br>+ JWT<br>+ is_just_registered=True
      Backend-api->>Frontend: data
      Frontend->>User: Показать форму<br>обязательного заполнения<br>профиля
    end
```

#### change-profile-settings-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant ChangeProfileSettingsUseCase

    User->>Frontend: Изменяет настройки
    User->>Frontend: Нажимает "Сохранить"
    Frontend->>Backend-api: PUT /profile
    Backend-api->>ChangeProfileSettingsUseCase: execute(data)
    ChangeProfileSettingsUseCase->>Backend-api: return msg
    Backend-api->>Frontend: data
    Frontend->>User: alert: msg
```

#### add-items-for-buy-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant AddItemsForBuyUseCase

    User->>Frontend: Выбирает предметы
    User->>Frontend: Нажимает кнопку
    Frontend->>Backend-api: POST /items/buy
    Backend-api->>AddItemsForBuyUseCase: execute(data)
    AddItemsForBuyUseCase->>Backend-api: return msg
    Backend-api->>Frontend: data
    Frontend->>User: alert: msg
    Frontend->>Frontend: Init CheckItemsUseCase
```

#### remove-items-for-buy-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant RemoveItemsForBuyUseCase

    User->>Frontend: Выбирает предметы
    User->>Frontend: Нажимает кнопку
    Frontend->>Backend-api: DELETE /items/buy
    Backend-api->>RemoveItemsForBuyUseCase: execute(data)
    RemoveItemsForBuyUseCase->>Backend-api: return msg
    Backend-api->>Frontend: data
    Frontend->>User: alert: msg
    Frontend->>Frontend: Init CheckItemsUseCase
```

#### change-items-for-buy-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant ChangeItemsForBuyUseCase

    User->>Frontend: Изменяет настройки предмета
    Frontend->>Backend-api: PUT /items/buy
    Backend-api->>ChangeItemsForBuyUseCase: execute(data)
    ChangeItemsForBuyUseCase->>Backend-api: return msg
    Backend-api->>Frontend: data
    Frontend->>User: alert: msg
    Frontend->>Frontend: Init CheckItemsUseCase
```

#### add-items-for-sell-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant AddItemsForSellUseCase

    User->>Frontend: Выбирает предметы
    User->>Frontend: Нажимает кнопку
    Frontend->>Backend-api: POST /items/sell
    Backend-api->>AddItemsForSellUseCase: execute(data)
    AddItemsForSellUseCase->>Backend-api: return msg
    Backend-api->>Frontend: data
    Frontend->>User: alert: msg
    Frontend->>Frontend: Init CheckItemsUseCase
```

#### remove-items-for-sell-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant RemoveItemsForSellUseCase

    User->>Frontend: Выбирает предметы
    User->>Frontend: Нажимает кнопку
    Frontend->>Backend-api: DELETE /items/sell
    Backend-api->>RemoveItemsForSellUseCase: execute(data)
    RemoveItemsForSellUseCase->>Backend-api: return msg
    Backend-api->>Frontend: data
    Frontend->>User: alert: msg
    Frontend->>Frontend: Init CheckItemsUseCase
```

#### change-items-for-sell-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    actor User
    participant Frontend
    participant Backend-api
    participant ChangeItemsForSellUseCase

    User->>Frontend: Изменяет настройки предмета
    Frontend->>Backend-api: PUT /items/sell
    Backend-api->>ChangeItemsForSellUseCase: execute(data)
    ChangeItemsForSellUseCase->>Backend-api: return msg
    Backend-api->>Frontend: data
    Frontend->>User: alert: msg
    Frontend->>Frontend: Init CheckItemsUseCase
```

#### check-items-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    participant Frontend
    participant Backend-api
    participant CheckItemsUseCase

    Frontend->>Backend-api: GET /items
    Backend-api->>CheckItemsUseCase: execute(data)
    CheckItemsUseCase->>Backend-api: return data
    Backend-api->>Frontend: data
    Frontend->>Frontend: update UI
```

### Backend

#### buy-item-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    AutoTradingService->>BuyItemUseCase: data
```

#### sell-item-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    AutoTradingService->>SellItemUseCase: data
```

#### notify-usecase

```mermaid
%%{init: {"theme": "dark"}}%%

sequenceDiagram
    ...->>NotifyUseCase: data
```
