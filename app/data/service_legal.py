"""Дисклеймер и источники права для страницы услуги."""

from __future__ import annotations

from urllib.parse import urlparse

_FAVICON_DIR = "/assets/icons/legal"

SERVICE_LEGAL_SOURCES = [
    {
        "title": (
            "Конституция Российской Федерации, статья 41. "
            "Право граждан на охрану здоровья и медицинскую помощь."
        ),
        "url": (
            "https://www.consultant.ru/document/cons_doc_LAW_28399/"
            "8c815f376c72a61b3df7905bb5aae9f144d2cb0d/"
        ),
    },
    {
        "title": (
            "Федеральный закон № 323-ФЗ «Об основах охраны здоровья граждан "
            "в Российской Федерации». Основной закон, регулирующий медицинскую "
            "деятельность и права пациентов."
        ),
        "url": "https://www.consultant.ru/document/cons_doc_LAW_121895/",
    },
    {
        "title": (
            "Министерство здравоохранения Российской Федерации. "
            "Официальный государственный орган в сфере здравоохранения."
        ),
        "url": "https://minzdrav.gov.ru/",
    },
    {
        "title": (
            "Росздравнадзор, единый реестр лицензий. "
            "Государственная проверка медицинских лицензий."
        ),
        "url": "https://roszdravnadzor.gov.ru/services/licenses",
    },
    {
        "title": (
            "Рубрикатор клинических рекомендаций Минздрава России. "
            "Официальная база российских клинических рекомендаций."
        ),
        "url": "https://cr.minzdrav.gov.ru/clin-rec",
    },
    {
        "title": (
            "Постановление Правительства РФ № 659 от 30.05.2026. "
            "Правила предоставления платных медицинских услуг, "
            "действующие с 1 сентября 2026 года."
        ),
        "url": "https://www.consultant.ru/document/cons_doc_LAW_535622/",
    },
    {
        "title": (
            "Закон РФ № 2300-1 «О защите прав потребителей». "
            "Права пациентов как потребителей платных медицинских услуг."
        ),
        "url": "https://www.consultant.ru/document/cons_doc_LAW_305/",
    },
    {
        "title": (
            "Федеральный закон № 152-ФЗ «О персональных данных». "
            "Обработка и конфиденциальность персональных данных пациентов."
        ),
        "url": "https://www.consultant.ru/document/cons_doc_LAW_61801/",
    },
    {
        "title": (
            "Федеральный закон № 99-ФЗ «О лицензировании отдельных видов деятельности». "
            "Общие требования к лицензируемой деятельности, включая медицинскую."
        ),
        "url": "https://www.consultant.ru/document/cons_doc_LAW_113658/",
    },
    {
        "title": (
            "Постановление Правительства РФ № 852 от 01.06.2021 "
            "«О лицензировании медицинской деятельности». "
            "Специальные лицензионные требования к медицинским организациям."
        ),
        "url": "https://www.consultant.ru/document/cons_doc_LAW_385633/",
    },
]


def _host_key(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def get_service_legal() -> dict:
    sources = []
    for item in SERVICE_LEGAL_SOURCES:
        host = _host_key(item["url"])
        sources.append(
            {
                **item,
                "host": host,
                "favicon": f"{_FAVICON_DIR}/{host}.png",
            }
        )

    return {"sources": sources}
