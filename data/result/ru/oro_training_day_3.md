# OroCommerce Training – Day 3 (таймкоды и структура)

(Временные диапазоны приблизительные, сгруппированы по логическим блокам сессии.)

## Введение и организационные моменты  
**00:00 – 00:03**  
* Приветствие, проверка присутствия.  
* Возврат к месту остановки предыдущего дня.  
* План: практика + теория (решено сначала теория по голосованию).  

## Рекап: Сущности, Репозитории, Расширяемость  
**00:03 – 00:12**  
* Создание пользовательской сущности, использование EntityRepository.  
* Получение репозитория: ManagerRegistry vs DoctrineHelper (короткий путь).  
* Делание сущности configurable (вкл./выкл. функциональность из UI и кодом).  
* Расширяемые (extend) и расширенные (extended) сущности: добавление полей и связей к core.  
* Entity alias: автогенерация, возможность переопределения.  

## Installers vs Migrations: Поток и размещение  
**00:12 – 00:18**  
* Installer: полная схема при первой установке.  
* Migrations: пошаговые изменения (версии).  
* Структура каталогов: Migrations/Schema + Version*.  
* Использование Schema объектa для создания/изменения таблиц и post queries.  
* Команда: `oro:migration:load --force` (safety switch).  

## Data Fixtures (обычные данные)  
**00:18 – 00:27**  
* Назначение: обязательные “недемо” данные (пример: product units).  
* Doctrine Fixtures: создание объектов, заполнение, persist + flush.  
* Расположение: Migrations/Data/ORM.  
* Именование файлов произвольное.  

## Data Fixtures: Зависимости, Порядок, Версионность  
**00:27 – 00:35**  
* DependentFixtureInterface: гарантированный порядок между бандлами (пример: Users после Organizations).  
* OrderedFixtureInterface: порядок внутри одного набора.  
* VersionedFixtureInterface: повторная загрузка при изменении версии (пример email templates).  
* Изменение версии (getVersion) для повторного применения.  

## Команды загрузки фикстур и режимы  
**00:35 – 00:39**  
* `oro:migration:data:load` — мгновенное выполнение (без force).  
* `--dry-run` для просмотра списка.  
* Типы: обычные (ORM) и демо (`--fixtures-type=demo`).  
* Demo fixtures: расположение Migrations/Data/Demo/ORM, загружаются только при явном указании.  
* Возможность догрузить демо после чистой установки.  
* Фильтрация по бандлу (switch bundle) — осторожно из-за кросс-зависимостей core.  

## Отличие обычных и Demo Fixtures  
**00:39 – 00:44**  
* Обычные: обязательны для работы (единицы, конфигурации).  
* Demo: пример наполнения (продукты, пользователи) — не нужны на проде.  

## Best Practices по сущностям и расширениям  
**00:44 – 00:49**  
* Для своих сущностей — обычные Doctrine поля (не extended).  
* Extended поля использовать только для добавления к core или когда нет доступа к исходнику.  
* Двусторонние связи: помнить о методах для owning/inverse стороны.  

## Производительность и Гидратация  
**00:49 – 00:53**  
* Doctrine object hydration может быть медленным на больших объёмах.  
* Оптимизация: array hydration → при необходимости raw SQL.  

## Изменение Doctrine метаданных  
**00:53 – 00:57**  
* Нельзя править vendor-код.  
* Слушатель события `loadClassMetadata` для модификации mapping (аннотации / поля / связи).  

## Переход к теме Data Grid  
**00:57 – 01:00**  
* Цель: после создания сущности — отобразить список (index page).  
* Нужны: шаблон, контроллер/экшен, data grid конфигурация, пункт меню.  

## Data Grid: Концепция и Источники  
**01:00 – 01:05**  
* Универсальный список: источники ORM / Search / Array.  
* Использование на storefront (PLP / категории) через сильно кастомизированную сетку.  
* Расширяемость и независимость от конкретного источника.  

## Data Grid: YAML Конфигурация (структура)  
**01:05 – 01:17**  
* Файл: `Resources/config/oro/datagrids.yml`.  
* Ключ `datagrids:` → имя гряда (уникально).  
* `extended_entity_name` для поддержки динамических (extended) полей.  
* `source` (type, query: select/from/where/group).  
* `columns`, `sorters`, `filters`, `properties`, `actions` (row & mass).  
* Свойства для построения ссылок (ID, view_link, update_link).  
* Динамическая генерация URL через route + параметры.  
* Массовые/строковые действия и защита ACL.  

## Рендеринг Ячеек и Twig  
**01:17 – 01:23**  
* Тип колонки `twig` + `frontend_type: html` + `template`.  
* В шаблон передаются: `value` (значение ячейки), `record` (вся строка, `record.getValue('column')`).  

## Расширение и Переопределение Grids  
**01:23 – 01:28**  
* Мердж YAML по порядку загрузки бандлов.  
* Локальное переопределение: определить тот же grid name с частичной секцией.  
* `extends:` для наследования конфигураций похожих гридов.  
* События: build_before, build_after, result_before, result_after — для сложной логики.  
* Grid extensions: вынос функционала (pagination и др.) в отдельные расширения.  

## Пример Модификации (Отключение Фильтра)  
**01:28 – 01:32**  
* Создать свой `datagrids.yml`, указать grid → filters → <column>: disabled: true.  
* Нет необходимости копировать всю конфигурацию.  

## Index Page (Контроллер и Шаблон)  
**01:32 – 01:38**  
* Контроллер (PaymentTermController) + action index.  
* Аннотации маршрутов (type: annotation) + `routing.yml` ресурс с prefix.  
* Автопоиск шаблона: `Resources/views/<ControllerName>/<action>.html.twig`.  
* Базовый шаблон index: расширение базового и передача `gridName`.  
* Минимальный шаблон: extends + параметр сетки.  

## Маршруты и Именование  
**01:38 – 01:41**  
* Конвенция: `oro_<entity>_<action>` (например: `oro_payment_term_index`, `oro_payment_term_view`).  
* Prefix для группы маршрутов в routing.yml.  

## Меню (Navigation / KnpMenu)  
**01:41 – 01:47**  
* Файл: `navigation.yml` (namespace: navigation → menu_config).  
* `items:` — определение узлов (label, route, position, icon, extras).  
* `tree:` — размещение в нужном меню (application_menu …).  
* Wildcard `routes:` для подсветки активного пункта на связанных страницах (index + view).  
* Пункты без route (контейнеры / заголовки).  

## Размещение Пункта Меню  
**01:47 – 01:51**  
* Вставка в: application_menu → system → user_management (пример).  
* Управление порядком через position.  
* Иконки и подсветка через extras / routes.  

## Краткое Резюме Дня  
* Повторили расширяемость и конфигурируемость сущностей.  
* Разобрали различия installer vs migrations.  
* Изучили обычные и demo fixtures, их жизненный цикл и команды.  
* Рассмотрели зависимости, порядок и версионность фикстур.  
* Обсудили best practices и производительность Doctrine.  
* Показали изменение метаданных через слушатель.  
* Глубоко разобрали Data Grid: структура, источники, действия, расширение.  
* Настройка отображения колонок через Twig (value + record).  
* События и расширения для динамических модификаций.  
* Построили index page + маршруты + меню.  

## Ключевые Команды  
* `oro:migration:load --force`  
* `oro:migration:data:load [--dry-run] [--fixtures-type=demo] [--bundle=...]`  

## Основные Интерфейсы Fixtures  
* DependentFixtureInterface  
* OrderedFixtureInterface  
* VersionedFixtureInterface  

## Важные События  
* Doctrine: loadClassMetadata  
* DataGrid: build_before / build_after / result_before / result_after  

## Быстрый Таймлайн (укрупненно)  
* 00:00 – 00:12 Рекап сущностей и репозиториев  
* 00:12 – 00:18 Installers vs Migrations  
* 00:18 – 00:27 Data Fixtures (ORM)  
* 00:27 – 00:35 Зав. / Порядок / Версии фикстур  
* 00:35 – 00:44 Команды и demo fixtures  
* 00:44 – 00:53 Best practices, производительность  
* 00:53 – 00:57 Doctrine metadata listener  
* 00:57 – 01:17 Data Grid базовая структура  
* 01:17 – 01:28 Twig рендеринг, расширение, события  
* 01:28 – 01:38 Index page + routing  
* 01:38 – 01:47 Меню и навигация  
* 01:47 – 01:51 Финальные штрихи и резюме  

## Полезные Паттерны  
* extended_entity_name для динамических полей  
* properties + routes для построения action ссылок  
* disabled: true для отключения фильтра  
* value / record в Twig для ячеек  

## Следующие Шаги (ожидаемо)  
* CRUD: View / Update / Delete (глобальные действия).  
* ACL и безопасность.  
* Формы и