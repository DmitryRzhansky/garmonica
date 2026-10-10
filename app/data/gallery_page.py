"""Данные страницы «Фотогалерея» — фото из блока стационара."""

from __future__ import annotations

from app.data.service_facility import FACILITY_PHOTOS


def get_gallery_page() -> dict:
    return {
        "photos": list(FACILITY_PHOTOS),
    }
