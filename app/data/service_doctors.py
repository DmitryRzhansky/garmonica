"""Врачи для блока «Наши врачи» на страницах услуг."""

from app.data.doctors import get_clinic_doctors


def get_service_doctors() -> list[dict]:
    return get_clinic_doctors()
