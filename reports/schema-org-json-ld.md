# Отчёт: Schema.org / JSON-LD

Ветка: `feat/schema-org-json-ld`  
Базовый коммит: `9a565e0ffbc9f99d26617e93efd1592c6beed3cb`

## 1. Покрытие страниц

Пересчитано перед внедрением и подтверждено тестами:

| Категория | Количество |
|---|---|
| Услуги `structural` | 1 |
| Услуги `silo-root` | 12 |
| Услуги `child` | 138 |
| Услуги `geo-hub` | 10 |
| Услуги `metro` | 860 |
| Услуги `okrug` | 60 |
| Услуги `city` | 420 |
| **Услуги всего** | **1501** |
| Информационные (`INFO_PAGES`) | 11 |
| Главная `/` | 1 |
| **Публичные HTML всего** | **1513** |

Все 1513 URL отдают HTTP 200 и ровно один блок `application/ld+json` с `@graph`.  
Страницы 404 JSON-LD не содержат.

## 2. Применённые типы Schema.org

| Страницы | Типы |
|---|---|
| `/` | `WebSite`, `WebPage`, `MedicalClinic`, `ItemList` |
| `/uslugi/` | `CollectionPage`, `ItemList`, `FAQPage`, `BreadcrumbList`, `MedicalClinic` |
| Сило/child услуг | `WebPage`, `Service`, `FAQPage`, `BreadcrumbList`, `MedicalClinic` |
| Геостраницы | то же + `areaServed` (`Place` / `AdministrativeArea` / `City`) |
| `/voprosy/` | `FAQPage` (документ), `BreadcrumbList`, `MedicalClinic` |
| `/otzyvy/` | `CollectionPage`, `ItemList`, `CreativeWork`, `MedicalClinic` |
| `/vrachi/` | `CollectionPage`, `ItemList`, `Person`, `MedicalClinic` |
| `/ceny/` | `CollectionPage`, `OfferCatalog`, `Offer`, `MedicalClinic` |
| `/o-klinike/` | `AboutPage`, `MedicalClinic` |
| `/kontakty/` | `ContactPage`, `MedicalClinic` |
| `/licenziya/` | `WebPage`, `MedicalClinic` |
| `/galereya/` | `ImageGallery`, `ImageObject`, `ItemList`, `MedicalClinic` |
| `/karta-sajta/` | `CollectionPage`, `ItemList`, `MedicalClinic` |
| Юридические | `WebPage`, `MedicalClinic` |

Единый стабильный `@id` клиники: `{host}/#clinic` (`MedicalClinic`).  
Отдельные независимые `Organization` / `LocalBusiness` не создавались.

## 3. Google rich results vs Schema.org

| Разметка | Schema.org | Google rich result (на момент внедрения) |
|---|---|---|
| `BreadcrumbList` | да | поддерживается |
| `Organization` / `MedicalClinic` (админ. сведения) | да | knowledge panel / disambiguation; не звёзды |
| `FAQPage` | да | **не показывается** с 7 мая 2026; разметка сохранена |
| `Review` / `AggregateRating` у клиники | сознательно не используется | self-serving reviews для LocalBusiness недоступны |
| `Service`, `OfferCatalog`, `Person`, `ImageGallery` | да | отдельного rich result обычно нет; это не ошибка Schema.org |

Внешние ручные прогоны Rich Results Test / validator.schema.org по всем URL в этой среде не выполнялись (интерактивный UI). Локально проверены JSON-синтаксис, `@graph`, `@id`, canonical и регрессия HTML.

## 4. FAQ

- Прежние inline-блоки в `service-faq.html` и `faq.html` перенесены в единый серверный `@graph` (без второго `FAQPage`).
- На `/voprosy/` документ типизирован как `FAQPage` (без параллельного `WebPage`).
- На страницах услуг: `WebPage`/`CollectionPage` + `FAQPage` с `@id` `{url}#faq`, связь через `hasPart`.
- Тесты подтверждают: 10 вопросов на услугах; на `/voprosy/` тексты `Question.name` / `Answer.text` совпадают с `faq_page.py` по порядку.

## 5. Отзывы и рейтинги

Внедрено на `/otzyvy/`:

- `CollectionPage` + `ItemList`
- элементы как `CreativeWork` с `author`, `text`, указанием площадки (`isPartOf.name`)

Пропущено и почему:

| Свойство | Причина |
|---|---|
| `Review` | даты без года; нет подтверждённых URL первоисточника; риск недостоверных Review-объектов |
| `reviewRating` / `AggregateRating` | self-serving reviews; сводные баллы площадок не должны становиться рейтингом клиники |
| `review` / `aggregateRating` у `MedicalClinic` и `Service` | запрещено ТЗ и политикой Google |
| `datePublished` | в данных только день+месяц без года |

Видимые отзывы и UI не изменялись.

## 6. Тестирование JSON-LD

`tests/test_structured_data.py`:

- обход всех 1513 URL: статус 200, валидный JSON, один `@graph`, уникальные `@id` в графе, один `@id` клиники на сайте, `url` страницы = canonical;
- репрезентативные типы по категориям;
- FAQ / цены / врачи / geo `areaServed` без филиалов;
- отсутствие JSON-LD на 404;
- регрессия HTML: SHA-256 после удаления `script[type="application/ld+json"]` совпадает с эталоном `tests/fixtures/html_content_fingerprints.json`.

Полный прогон: `pytest` → **55 passed**.

## 7. Сравнение HTML до и после

Эталон снят с шаблонов `main` (без JSON-LD injection).  
После внедрения сравнение выполняется с исключением только `script[type="application/ld+json"]`.

Результат: расхождений вне JSON-LD нет (тест `test_html_content_unchanged_except_json_ld`).

## 8. Изменённые и добавленные файлы

**Изменены**

- `app/__init__.py` — context processor JSON-LD
- `app/templates/base.html` — вывод одного JSON-LD в `<head>`
- `app/templates/components/service-faq.html` — удален дублирующий FAQ JSON-LD
- `app/templates/pages/faq.html` — удален дублирующий FAQ JSON-LD

**Добавлены**

- `app/services/structured_data/__init__.py`
- `app/services/structured_data/builder.py`
- `app/services/structured_data/clinic.py`
- `app/services/structured_data/offers.py`
- `app/services/structured_data/serialize.py`
- `tests/test_structured_data.py`
- `tests/fixtures/html_content_fingerprints.json`
- `scripts/capture_html_fingerprints.py`
- `scripts/recapture_baseline.py`
- `reports/schema-org-json-ld.md`

## 9. Пропущенные свойства (сводка)

| Свойство | Почему пропущено |
|---|---|
| `geo` / координаты клиники | нет отдельного подтверждённого поля; координаты только внутри embed URL |
| `sameAs` для мессенджеров | заглушки (`t.me/`, `vk.com/`, `max.ru/`), не официальные профили |
| `image` врачей | иконки Phosphor не являются портретами |
| `Physician` | не подтверждён как точный тип для всех специалистов; используется `Person` |
| `offers` у `Service` | нет достоверного 1:1 соответствия услуги и строки прайса |
| `MedicalProcedure` / `MedicalTherapy` / `MedicalCondition` | не применять автоматически к наркологическим/психиатрическим услугам |
| `AggregateRating` / `Review` у клиники и услуг | self-serving + неполные метаданные отзывов |
| `searchAction` у `WebSite` | на сайте нет поиска |
| Отдельные URL-профили врачей | на сайте нет таких страниц |
| Юридический адрес как `address` | в `address` указан опубликованный фактический адрес приёма (Люблинская, 46); legal address остаётся в данных лицензии/реквизитов без дублирования филиалов |

## 10. Подтверждение ограничений ТЗ

- Пользовательские тексты, H1–H6, title/description/canonical не менялись.
- FAQ, отзывы, цены, данные врачей не редактировались.
- CSS/JS/изображения/маршруты/sitemap не менялись.
- Изменения только в генерации JSON-LD, минимальном подключении к шаблонам, переносе существующего FAQ JSON-LD и тестах/отчёте.
- Автоматический merge в `main` не выполняется.
