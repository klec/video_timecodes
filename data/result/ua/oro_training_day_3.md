# OroCommerce Training – День 3 (таймкоди та структура)

(Часові діапазони приблизні, згруповані за логічними блоками сесії.)

## Вступ і організаційні моменти  
**00:00 – 00:03**  
* Привітання, перевірка присутності.  
* Повернення до точки зупинки попереднього дня.  
* План: практика + теорія (вирішено спочатку теорія за голосуванням).  

## Рекап: Сутності, Репозиторії, Розширюваність  
**00:03 – 00:12**  
* Створення користувацької сутності, використання EntityRepository.  
* Отримання репозиторію: ManagerRegistry vs DoctrineHelper (скорочений шлях).  
* Робимо сутність configurable (вкл./викл. функціональність з UI і кодом).  
* Розширювані (extend) і розширені (extended) сутності: додавання полів і зв’язків до core.  
* Entity alias: автогенерація, можливість перевизначення.  

## Installers vs Migrations: Потік і розміщення  
**00:12 – 00:18**  
* Installer: повна схема при першій установці.  
* Migrations: покрокові зміни (версії).  
* Структура каталогів: Migrations/Schema + Version*.  
* Використання Schema об’єкта для створення/зміни таблиць і post queries.  
* Команда: `oro:migration:load --force` (safety switch).  

## Data Fixtures (звичайні дані)  
**00:18 – 00:27**  
* Призначення: обов’язкові “не демо” дані (приклад: product units).  
* Doctrine Fixtures: створення об’єктів, заповнення, persist + flush.  
* Розташування: Migrations/Data/ORM.  
* Іменування файлів довільне.  

## Data Fixtures: Залежності, Порядок, Версійність  
**00:27 – 00:35**  
* DependentFixtureInterface: гарантований порядок між бандлами (приклад: Users після Organizations).  
* OrderedFixtureInterface: порядок всередині одного набору.  
* VersionedFixtureInterface: повторне завантаження при зміні версії (приклад email templates).  
* Зміна версії (getVersion) для повторного застосування.  

## Команди завантаження фікстур і режими  
**00:35 – 00:39**  
* `oro:migration:data:load` — миттєве виконання (без force).  
* `--dry-run` для перегляду списку.  
* Типи: звичайні (ORM) і демо (`--fixtures-type=demo`).  
* Demo fixtures: розташування Migrations/Data/Demo/ORM, завантажуються тільки при явному вказанні.  
* Можливість догрузити демо після чистої установки.  
* Фільтрація по бандлу (switch bundle) — обережно через крос-залежності core.  

## Відмінність звичайних і Demo Fixtures  
**00:39 – 00:44**  
* Звичайні: обов’язкові для роботи (одиниці, конфігурації).  
* Demo: приклад наповнення (продукти, користувачі) — не потрібні на проді.  

## Best Practices по сутностях і розширеннях  
**00:44 – 00:49**  
* Для своїх сутностей — звичайні Doctrine поля (не extended).  
* Extended поля використовувати тільки для додавання до core або коли немає доступу до вихідника.  
* Двосторонні зв’язки: пам’ятати про методи для owning/inverse сторони.  

## Продуктивність і гідратація  
**00:49 – 00:53**  
* Doctrine object hydration може бути повільним на великих обсягах.  
* Оптимізація: array hydration → за потреби raw SQL.  

## Зміна Doctrine метаданих  
**00:53 – 00:57**  
* Не можна правити vendor-код.  
* Слухач події `loadClassMetadata` для модифікації mapping (анотації / поля / зв’язки).  

## Перехід до теми Data Grid  
**00:57 – 01:00**  
* Мета: після створення сутності — показати список (index page).  
* Потрібні: шаблон, контролер/action, data grid конфігурація, пункт меню.  

## Data Grid: Концепція і Джерела  
**01:00 – 01:05**  
* Універсальний список: джерела ORM / Search / Array.  
* Використання у storefront (PLP / категорії) через сильно кастомізовану сітку.  
* Розширюваність і незалежність від конкретного джерела.  

## Data Grid: YAML Конфігурація (структура)  
**01:05 – 01:17**  
* Файл: `Resources/config/oro/datagrids.yml`.  
* Ключ `datagrids:` → ім’я гріда (унікально).  
* `extended_entity_name` для підтримки динамічних (extended) полів.  
* `source` (type, query: select/from/where/group).  
* `columns`, `sorters`, `filters`, `properties`, `actions` (row & mass).  
* Властивості для побудови посилань (ID, view_link, update_link).  
* Динамічна генерація URL через route + параметри.  
* Масові/рядкові дії та захист ACL.  

## Рендеринг Комірок і Twig  
**01:17 – 01:23**  
* Тип колонки `twig` + `frontend_type: html` + `template`.  
* У шаблон передаються: `value` (значення комірки), `record` (весь рядок, `record.getValue('column')`).  

## Розширення і Перевизначення Grids  
**01:23 – 01:28**  
* Merge YAML за порядком завантаження бандлів.  
* Локальне перевизначення: визначити той самий grid name з частковою секцією.  
* `extends:` для наслідування конфігурацій схожих грідів.  
* Події: build_before, build_after, result_before, result_after — для складної логіки.  
* Grid extensions: виніс функціоналу (pagination тощо) у окремі розширення.  

## Приклад Модифікації (Вимкнення Фільтра)  
**01:28 – 01:32**  
* Створити свій `datagrids.yml`, вказати grid → filters → <column>: disabled: true.  
* Немає потреби копіювати всю конфігурацію.  

## Index Page (Контролер і Шаблон)  
**01:32 – 01:38**  
* Контролер (PaymentTermController) + action index.  
* Анотації маршрутів (type: annotation) + `routing.yml` ресурс з prefix.  
* Автопошук шаблону: `Resources/views/<ControllerName>/<action>.html.twig`.  
* Базовий шаблон index: розширення базового і передача `gridName`.  
* Мінімальний шаблон: extends + параметр сітки.  

## Маршрути і Іменування  
**01:38 – 01:41**  
* Конвенція: `oro_<entity>_<action>` (наприклад: `oro_payment_term_index`, `oro_payment_term_view`).  
* Prefix для групи маршрутів у routing.yml.  

## Меню (Navigation / KnpMenu)  
**01:41 – 01:47**  
* Файл: `navigation.yml` (namespace: navigation → menu_config).  
* `items:` — визначення вузлів (label, route, position, icon, extras).  
* `tree:` — розміщення в потрібному меню (application_menu …).  
* Wildcard `routes:` для підсвічування активного пункту на пов’язаних сторінках (index + view).  
* Пункти без route (контейнери / заголовки).  

## Розміщення Пункту Меню  
**01:47 – 01:51**  
* Вставка в: application_menu → system → user_management (приклад).  
* Керування порядком через position.  
* Іконки і підсвічування через extras / routes.  

## Коротке Резюме Дня  
* Повторили розширюваність і конфігурованість сутностей.  
* Розібрали відмінності installer vs migrations.  
* Вивчили звичайні і demo fixtures, їх життєвий цикл і команди.  
* Розглянули залежності, порядок і версійність фікстур.  
* Обговорили best practices і продуктивність Doctrine.  
* Показали зміну метаданих через слухач.  
* Глибоко розібрали Data Grid: структура, джерела, дії, розширення.  
* Налаштування відображення колонок через Twig (value + record).  
* Події і розширення для динамічних модифікацій.  
* Побудували index page + маршрути + меню.  

## Ключові Команди  
* `oro:migration:load --force`  
* `oro:migration:data:load [--dry-run] [--fixtures-type=demo] [--bundle=...]`  

## Основні Інтерфейси Fixtures  
* DependentFixtureInterface  
* OrderedFixtureInterface  
* VersionedFixtureInterface  

## Важливі Події  
* Doctrine: loadClassMetadata  
* DataGrid: build_before / build_after / result_before / result_after  

## Швидкий Таймлайн (укрупнено)  
* 00:00 – 00:12 Рекап сутностей і репозиторіїв  
* 00:12 – 00:18 Installers vs Migrations  
* 00:18 – 00:27 Data Fixtures (ORM)  
* 00:27 – 00:35 Зал. / Порядок / Версії фікстур  
* 00:35 – 00:44 Команди і demo fixtures  
* 00:44 – 00:53 Best practices, продуктивність  
* 00:53 – 00:57 Doctrine metadata listener  
* 00:57 – 01:17 Data Grid базова структура  
* 01:17 – 01:28 Twig рендеринг, розширення, події  
* 01:28 – 01:38 Index page + routing  
* 01:38 – 01:47 Меню і навігація  
* 01:47 – 01:51 Фінальні штрихи і резюме  

## Корисні Патерни  
* extended_entity_name для динамічних полів  
* properties + routes для побудови action-посилань  
* disabled: true для вимкнення фільтра  
* value / record у Twig для комірок  

## Наступні Кроки (очікувано)  
* CRUD: View / Update / Delete (глобальні дії).  
* ACL і безпека.  
* Форми і обробники.  
