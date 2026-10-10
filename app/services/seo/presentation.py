"""Кластер страницы: герой, форма, карточки отличий, вкладка прайса."""

from __future__ import annotations

from dataclasses import dataclass

from app.data.service_facility import normalize_service_url

HOME_MARKERS = (
    "/na-domu/",
    "/narkolog-na-dom/",
    "/psihiatr-na-dom/",
    "/kapelnitsy/",
)

INPATIENT_MARKERS = (
    "/stacionar/",
    "/v-stacionare/",
    "/gospitalizaciya/",
    "/chastnyj-vytrezvitel/",
)


@dataclass(frozen=True)
class HeroCopy:
    badge: str
    features: tuple[tuple[str, str], tuple[str, str], tuple[str, str]]
    price_label: str
    price_value: str
    mode_label: str
    mode_value: str
    cta: str


@dataclass(frozen=True)
class FormCopy:
    title: str
    aria: str
    button: str
    show_address: bool


@dataclass(frozen=True)
class DiffCard:
    before: str
    accent: str
    after: str
    text: str


def presentation_of(url: str) -> str:
    current = normalize_service_url(url)
    if current == "/uslugi/":
        return "catalog"
    if "/reabilitaciya/" in current:
        return "rehab"
    if "/onlajn" in current:
        return "online"
    if "/kodirovanie/" in current and "/na-domu/" not in current:
        return "coding"
    if any(marker in current for marker in HOME_MARKERS):
        return "home"
    if any(marker in current for marker in INPATIENT_MARKERS):
        return "inpatient"
    if "/psihiatriya/" in current or "/psihoterapiya" in current:
        return "clinic"
    return "treatment"


def title_tail(url: str, presentation: str) -> str:
    if "/kapelnitsy/" in url:
        return "анонимно, выезд 30–60 минут, от 5 000 ₽"
    tails = {
        "home": "анонимно, выезд 30–60 минут, от 8 000 ₽",
        "inpatient": "круглосуточное наблюдение, от 12 000 ₽/сутки",
        "coding": "анонимно, после консультации",
        "rehab": "анонимно",
        "online": "анонимно, без выезда, 8 000 ₽",
        "catalog": "приём, выезд и стационар",
    }
    return tails.get(presentation, "анонимно, приём в клинике, 8 000 ₽")


def price_tab_for(url: str, presentation: str) -> str:
    if "/kapelnitsy/" in url:
        return "procedures"
    if presentation == "inpatient":
        return "stationary"
    return "consultations"


def facility_title_override(url: str) -> str | None:
    current = normalize_service_url(url)
    if any(marker in current for marker in HOME_MARKERS):
        return None
    if any(marker in current for marker in INPATIENT_MARKERS):
        return None
    if (
        "/psihiatriya/" in current
        or "/psihoterapiya" in current
        or "/onlajn" in current
        or current == "/uslugi/"
    ):
        return "Клиника на Люблинской, 46"
    return None


def hero_for(presentation: str, drip: bool) -> HeroCopy:
    del drip
    if presentation == "home":
        return HeroCopy(
            badge="Бригада в вашем районе",
            features=(
                ("Приезд специалиста", "30–45 минут"),
                ("Оплата", "после помощи"),
                ("Полная анонимность", "без постановки на учёт"),
            ),
            price_label="Стоимость выезда",
            price_value="от 5\u00a0000\u00a0₽",
            mode_label="Выезд — круглосуточно",
            mode_value="24/7, без выходных",
            cta="Вызвать нарколога на дом",
        )
    if presentation == "inpatient":
        return HeroCopy(
            badge="Стационар на Люблинской, 46",
            features=(
                ("Питание", "входит в сутки"),
                ("Срок", "3–21 день по состоянию"),
                ("Наблюдение", "дежурный врач"),
            ),
            price_label="Палата",
            price_value="от 12 000 ₽/сутки",
            mode_label="Стационар",
            mode_value="круглосуточно",
            cta="Заявка на госпитализацию",
        )
    if presentation == "online":
        return HeroCopy(
            badge="Онлайн-консультация",
            features=(
                ("Формат", "без выезда"),
                ("Дальше", "очный приём, если нужен"),
                ("Консультация", "8 000 ₽"),
            ),
            price_label="Консультация",
            price_value="8 000 ₽",
            mode_label="Формат",
            mode_value="без выезда на дом",
            cta="Записаться",
        )
    if presentation == "rehab":
        return HeroCopy(
            badge="Реабилитация",
            features=(
                ("Программа", "условия уточняют"),
                ("Запись", "после разговора"),
                ("Палаты клиники", "это не сама программа"),
            ),
            price_label="Стоимость",
            price_value="уточняют отдельно",
            mode_label="Условия",
            mode_value="до записи не фиксируют",
            cta="Отправить заявку",
        )
    if presentation == "coding":
        return HeroCopy(
            badge="Кодирование после консультации",
            features=(
                ("Сначала", "осмотр и согласие"),
                ("Метод", "выбирает врач"),
                ("Запой", "кодирование его не снимает"),
            ),
            price_label="Стоимость",
            price_value="после консультации",
            mode_label="Формат",
            mode_value="клиника или выезд, если врач согласует",
            cta="Записаться",
        )
    if presentation == "catalog":
        return HeroCopy(
            badge="Клиника на Люблинской, 46",
            features=(
                ("Форматы", "выезд, приём, стационар"),
                ("Консультация", "8 000 ₽"),
                ("Старт", "описание ситуации по телефону"),
            ),
            price_label="Консультация",
            price_value="8 000 ₽",
            mode_label="Запись",
            mode_value="круглосуточно",
            cta="Записаться",
        )
    if presentation == "clinic":
        return HeroCopy(
            badge="Клиника на Люблинской, 46",
            features=(
                ("На приёме", "осмотр и рекомендации"),
                ("Госпитализация", "только с согласия"),
                ("Консультация", "8 000 ₽"),
            ),
            price_label="Консультация психиатра",
            price_value="8 000 ₽",
            mode_label="Запись",
            mode_value="круглосуточно",
            cta="Записаться",
        )
    return HeroCopy(
        badge="Приём в клинике",
        features=(
            ("Старт", "консультация врача"),
            ("Дальше", "амбулаторно или стационар"),
            ("Консультация", "8 000 ₽"),
        ),
        price_label="Консультация нарколога",
        price_value="8 000 ₽",
        mode_label="Запись",
        mode_value="круглосуточно",
        cta="Записаться",
    )


def form_for(presentation: str) -> FormCopy:
    if presentation == "home":
        return FormCopy(
            title="Вызвать врача на дом",
            aria="Вызвать врача на дом",
            button="Вызвать врача",
            show_address=True,
        )
    if presentation == "inpatient":
        return FormCopy(
            title="Заявка на госпитализацию",
            aria="Заявка на госпитализацию",
            button="Отправить заявку",
            show_address=False,
        )
    if presentation == "online":
        return FormCopy(
            title="Запись на онлайн-консультацию",
            aria="Запись на онлайн-консультацию",
            button="Записаться",
            show_address=False,
        )
    if presentation == "rehab":
        return FormCopy(
            title="Уточнить программу реабилитации",
            aria="Уточнить программу реабилитации",
            button="Отправить заявку",
            show_address=False,
        )
    return FormCopy(
        title="Записаться на приём",
        aria="Записаться на приём",
        button="Записаться",
        show_address=False,
    )


def diff_cards_for(presentation: str, drip: bool) -> tuple[DiffCard, DiffCard, DiffCard, DiffCard]:
    if presentation == "home" and drip:
        return (
            DiffCard("Сначала", "осмотр", "а не готовый состав", "Капельницу не собирают по телефонному заказу. Врач смотрит состояние и только потом решает, нужна ли инфузия."),
            DiffCard("Это", "одна процедура", "а не весь курс", "Инфузия помогает при текущем состоянии. Зависимость одним визитом не лечат."),
            DiffCard("Если дома", "уже небезопасно", "", "Врач говорит, когда нужен стационар, и не проводит на адресе тот объём, который там небезопасен."),
            DiffCard("Сумму", "называют до начала", "", "Стоимость процедуры известна заранее. Дополнительные назначения после осмотра обсуждают отдельно."),
        )
    if presentation == "home":
        return (
            DiffCard("Приезжаем", "тихо, без сирен", "и яркой «скорой»", "Обычный автомобиль, без мигалок и лишнего шума у подъезда, чтобы не привлекать внимание соседей."),
            DiffCard("Всё нужное", "уже в укладке", "", "Расходники для осмотра и назначенной помощи везут с собой, а не отправляют семью в ночную аптеку."),
            DiffCard("Один врач", "ведёт осмотр", "", "Оценку состояния и решение, что можно сделать дома, принимает врач на вызове, а не диспетчер."),
            DiffCard("Дальше", "понятные рекомендации", "", "После визита семье говорят, что наблюдать и когда нужна повторная связь или стационар."),
        )
    if presentation == "inpatient":
        return (
            DiffCard("В палате", "дежурный врач", "и медсестра", "Стационар работает без выходных: на месте есть дежурный врач, медсестра и санитар."),
            DiffCard("Питание", "входит в сутки", "", "Четырёхразовое питание включено в стоимость размещения, отдельно его не выставляют."),
            DiffCard("Срок", "от 3 до 21 дня", "", "Сколько лежать, решают по состоянию, а не по фиксированному пакету на все случаи."),
            DiffCard("В одном отделении", "телефон и посещения", "ограничены", "Так устроен регламент безопасности. Правила объясняют до госпитализации."),
        )
    if presentation == "online":
        return (
            DiffCard("Разговор", "без выезда", "", "Консультация идёт дистанционно. Бригаду на адрес по этому формату не отправляют."),
            DiffCard("Острый случай", "это не онлайн", "", "Если человеку плохо прямо сейчас, нужен осмотр или скорая, а не видеозвонок."),
            DiffCard("Очно", "в той же клинике", "", "Когда дистанционного разговора мало, предлагают приём на Люблинской."),
            DiffCard("Дальше", "решает врач", "", "После разговора становится ясно, нужны ли очный осмотр, наблюдение или другой формат."),
        )
    if presentation == "coding":
        return (
            DiffCard("Сначала", "консультация", "", "Метод не выбирают по названию услуги. Нужны осмотр и согласие пациента."),
            DiffCard("Кодирование", "не снимает запой", "", "Процедура не заменяет вывод из запоя и не считается всем лечением зависимости."),
            DiffCard("Без согласия", "процедуру не делают", "", "Даже если звонят родственники, вмешательство в обычной ситуации требует согласия самого человека."),
            DiffCard("После", "нужно наблюдение", "", "Врач говорит, что делать дальше, а не оставляет пациента один на один с процедурой."),
        )
    if presentation == "rehab":
        return (
            DiffCard("Программу", "уточняют до записи", "", "Распорядок, срок и адрес называют при записи, в общем описании их нет."),
            DiffCard("Это", "не палата клиники", "", "Размещение в стационаре на Люблинской само по себе программой не является."),
            DiffCard("Старт", "разговор о задаче", "", "Сначала понятно, о какой зависимости речь и готов ли человек обсуждать правила."),
            DiffCard("Обещаний", "готового срока нет", "", "Длительность не ставят заранее, пока программу не согласовали."),
        )
    if presentation == "clinic":
        return (
            DiffCard("Сначала", "очный приём", "а не вызов бригады", "Врач осматривает, формирует заключение и даёт рекомендации."),
            DiffCard("Госпитализация", "только после согласия", "", "Стационар обсуждают, если приёма недостаточно и человек на него согласен."),
            DiffCard("Приём", "на Люблинской, 46", "", "Очная консультация проходит в клинике, а не в местном филиале района."),
            DiffCard("Сведения", "не для посторонних", "", "Данные обращения не используют в рекламе и не передают без законного основания."),
        )
    if presentation == "catalog":
        return (
            DiffCard("Три формата", "выезд, приём, стационар", "", "Раздел помогает выбрать маршрут, а не смешивает все услуги в один вызов."),
            DiffCard("Старт", "описание ситуации", "", "По телефону понятно, нужен ли адрес, запись или разговор о госпитализации."),
            DiffCard("Клиника", "на Люблинской, 46", "", "Очный приём и стационар проходят по одному адресу, без сети филиалов."),
            DiffCard("Дальше", "решает врач", "", "Процедуру не назначают по названию раздела. Сначала врач смотрит состояние."),
        )
    return (
        DiffCard("Сначала", "консультация", "", "Формат помощи выбирают после осмотра, а не по названию услуги."),
        DiffCard("Дальше", "приём или стационар", "", "Амбулаторное ведение и госпитализация — разные сценарии. Их не смешивают в одну услугу."),
        DiffCard("Кодирование", "отдельный шаг", "", "Его не подставляют вместо лечения и не обещают как способ снять запой."),
        DiffCard("Согласие", "нужно от пациента", "", "Звонок родственника описывает ситуацию, но не заменяет согласие человека."),
    )
