"""Stable MedicalClinic entity shared across the site."""

from __future__ import annotations

from typing import Any

from app.data.clinic_contacts import get_clinic_contacts
from app.data.license import get_clinic_license


def clinic_id(host: str) -> str:
    return f"{host}/#clinic"


def website_id(host: str) -> str:
    return f"{host}/#website"


def absolute_url(host: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return host.rstrip("/") + path


def build_medical_clinic(host: str) -> dict[str, Any]:
    contacts = get_clinic_contacts()
    license_data = get_clinic_license()
    logo_url = absolute_url(host, "/assets/images/logo-mark.png")

    specialties = sorted(
        {
            service
            for group in license_data["work_groups"]
            for entry in group["entries"]
            for service in entry["services"]
        }
    )

    return {
        "@type": "MedicalClinic",
        "@id": clinic_id(host),
        "name": contacts["brand"],
        "alternateName": f"{contacts['brand']} — {contacts['positioning']}",
        "legalName": contacts["legal_name"],
        "url": f"{host}/",
        "telephone": contacts["phone_tel"],
        "email": contacts["email"],
        "taxID": contacts["inn"],
        "identifier": [
            {
                "@type": "PropertyValue",
                "name": "ИНН",
                "value": contacts["inn"],
            },
            {
                "@type": "PropertyValue",
                "name": "ОГРН",
                "value": contacts["ogrn"],
            },
            {
                "@type": "PropertyValue",
                "name": "Номер лицензии",
                "value": license_data["number"],
            },
        ],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "ул. Люблинская, д. 46",
            "addressLocality": "Москва",
            "postalCode": "109387",
            "addressCountry": "RU",
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
            "opens": "00:00",
            "closes": "23:59",
        },
        "logo": logo_url,
        "image": logo_url,
        "medicalSpecialty": specialties,
        "hasCredential": {
            "@type": "EducationalOccupationalCredential",
            "name": "Лицензия на осуществление медицинской деятельности",
            "credentialCategory": "license",
            "identifier": license_data["number"],
            "recognizedBy": {
                "@type": "Organization",
                "name": license_data["authority"],
            },
            "url": absolute_url(host, "/licenziya/"),
        },
    }


def build_website(host: str) -> dict[str, Any]:
    contacts = get_clinic_contacts()
    return {
        "@type": "WebSite",
        "@id": website_id(host),
        "url": f"{host}/",
        "name": contacts["brand"],
        "inLanguage": "ru-RU",
        "publisher": {"@id": clinic_id(host)},
    }
