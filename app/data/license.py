"""Лицензия и выписка из реестра Росздравнадзора."""

from __future__ import annotations

from app.data.clinic_contacts import CLINIC_CONTACTS

LICENSE_NUMBER = "Л041-01137-77/01838787"
LICENSE_ISSUED_AT = "10.02.2025"
LICENSE_AUTHORITY = "Департамент здравоохранения города Москвы"
LICENSE_STATUS = "действует"
LICENSE_ORDER_ISSUE = "№ 211-Л от 10.02.2025"
LICENSE_ORDER_REISSUE = "№ 407-Л от 12.03.2025"
LICENSE_NOMENCLATURE = "Приказ Минздрава России № 866н"
LICENSE_PDF = "/assets/docs/license-L041-01137-77-01838787.pdf"
LICENSE_REGISTRY_URL = "https://roszdravnadzor.gov.ru/services/licenses"

LICENSE_LEGAL_ADDRESS = (
    "127018, г. Москва, вн.тер.г. муниципальный округ Марьина Роща, "
    "проезд Марьиной Рощи 3-й, д. 40, стр. 1, помещ. 22/22"
)

LICENSE_DOCUMENTS = [
    {
        "title": "Выписка из реестра лицензий",
        "label": "Выписка из реестра лицензий",
        "meta": "Страница 1 из 3",
        "image": "/assets/images/licenses/license-extract-page-1.png",
        "alt": "Выписка из реестра лицензий, страница 1",
        "width": 1190,
        "height": 1584,
    },
    {
        "title": "Выписка из реестра лицензий",
        "label": "Выписка из реестра лицензий, стр. 2",
        "meta": "Страница 2 из 3",
        "image": "/assets/images/licenses/license-extract-page-2.png",
        "alt": "Выписка из реестра лицензий, страница 2",
        "width": 1190,
        "height": 1584,
    },
    {
        "title": "Выписка из реестра лицензий",
        "label": "Выписка из реестра лицензий, стр. 3",
        "meta": "Страница 3 из 3",
        "image": "/assets/images/licenses/license-extract-page-3.png",
        "alt": "Выписка из реестра лицензий, страница 3",
        "width": 1190,
        "height": 1584,
    },
]

# Работы (услуги) из выписки — по Приказу 866н.
LICENSE_WORK_GROUPS = [
    {
        "title": "Первичная медико-санитарная помощь",
        "entries": [
            {
                "condition": (
                    "Первичная доврачебная медико-санитарная помощь "
                    "в амбулаторных условиях"
                ),
                "services": ["Сестринское дело"],
            },
            {
                "condition": (
                    "Первичная врачебная медико-санитарная помощь "
                    "в амбулаторных условиях"
                ),
                "services": ["Терапия"],
            },
            {
                "condition": (
                    "Первичная врачебная медико-санитарная помощь "
                    "в условиях дневного стационара"
                ),
                "services": ["Терапия"],
            },
            {
                "condition": (
                    "Первичная специализированная медико-санитарная помощь "
                    "в амбулаторных условиях"
                ),
                "services": [
                    "Неврология",
                    "Психиатрия-наркология",
                    "Функциональная диагностика",
                ],
            },
        ],
    },
    {
        "title": "Специализированная медицинская помощь",
        "entries": [
            {
                "condition": (
                    "Специализированная медицинская помощь "
                    "в условиях дневного стационара"
                ),
                "services": ["Сестринское дело"],
            },
            {
                "condition": (
                    "Специализированная медицинская помощь "
                    "в стационарных условиях"
                ),
                "services": ["Психиатрия-наркология", "Психотерапия"],
            },
        ],
    },
    {
        "title": "Скорая медицинская помощь",
        "entries": [
            {
                "condition": "Скорая медицинская помощь вне медицинской организации",
                "services": ["Скорая медицинская помощь"],
            },
            {
                "condition": (
                    "Скорая специализированная медицинская помощь "
                    "вне медицинской организации"
                ),
                "services": ["Психиатрия", "Психиатрия-наркология"],
            },
        ],
    },
    {
        "title": "Медицинские экспертизы и осмотры",
        "entries": [
            {
                "condition": "Медицинские экспертизы",
                "services": ["Экспертиза временной нетрудоспособности"],
            },
            {
                "condition": "Медицинские осмотры",
                "services": [
                    "Медицинские осмотры "
                    "(предсменные, предрейсовые, послесменные, послерейсовые)"
                ],
            },
        ],
    },
]


def get_clinic_license() -> dict:
    return {
        "number": LICENSE_NUMBER,
        "issued_at": LICENSE_ISSUED_AT,
        "authority": LICENSE_AUTHORITY,
        "status": LICENSE_STATUS,
        "order_issue": LICENSE_ORDER_ISSUE,
        "order_reissue": LICENSE_ORDER_REISSUE,
        "nomenclature": LICENSE_NOMENCLATURE,
        "pdf_url": LICENSE_PDF,
        "registry_url": LICENSE_REGISTRY_URL,
        "legal_name": CLINIC_CONTACTS["legal_name"],
        "inn": CLINIC_CONTACTS["inn"],
        "ogrn": CLINIC_CONTACTS["ogrn"],
        "legal_address": LICENSE_LEGAL_ADDRESS,
        "activity_address": CLINIC_CONTACTS["address_full"],
        "documents": list(LICENSE_DOCUMENTS),
        "work_groups": list(LICENSE_WORK_GROUPS),
    }
