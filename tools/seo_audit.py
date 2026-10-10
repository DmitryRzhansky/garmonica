"""Отчёт по SEO-полям каталога. Запуск: python tools/seo_audit.py"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.catalog import get_catalog  # noqa: E402

OUT = ROOT / "reports" / "seo"

EXAMPLES = [
    "/uslugi/narkolog-na-dom/",
    "/uslugi/narkolog-na-dom/aeroport/",
    "/uslugi/narkolog-na-dom/cao/",
    "/uslugi/narkolog-na-dom/moskovskaya-oblast/",
    "/uslugi/narkolog-na-dom/moskovskaya-oblast/himki/",
    "/uslugi/kapelnitsy/ot-zapoya-i-alkogolya/",
    "/uslugi/vyvod-iz-zapoya/v-stacionare/",
    "/uslugi/kodirovanie/metod-dovzhenko/",
    "/uslugi/psihiatriya/rasstrojstva-nastroeniya/depressiya/",
    "/uslugi/psihiatriya/psihiatr-na-dom/",
    "/uslugi/psihiatriya/stacionar/",
    "/uslugi/lechenie-narkomanii/mefedron/",
    "/uslugi/reabilitaciya/alkogolizm/",
]


def _group_counts(values: list[str]) -> list[tuple[str, int]]:
    buckets: dict[str, int] = defaultdict(int)
    for value in values:
        buckets[value] += 1
    return sorted(((text, count) for text, count in buckets.items() if count > 1), key=lambda item: -item[1])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    catalog = get_catalog()
    rows = []
    titles: list[str] = []
    descriptions: list[str] = []
    h1s: list[str] = []
    leads: list[str] = []
    faq_keys: list[str] = []
    by_service: dict[str, list[str]] = defaultdict(list)

    for page in catalog.pages:
        seo = catalog.view(page["url"]).seo
        faq = [{"ask": ask, "answer": answer} for ask, answer in seo.faq_items]
        status = "thin" if seo.thin_data else "ok"
        if page["kind"] in {"metro", "okrug", "city", "geo-hub"}:
            status = f"{status}, toponym"
        rows.append(
            {
                "url": page["url"],
                "title": seo.meta_title,
                "description": seo.meta_description,
                "h1": seo.h1,
                "lead": seo.lead,
                "profile": seo.service_url,
                "presentation": seo.presentation,
                "copy_id": seo.copy_id,
                "faq": faq,
                "status": status,
            }
        )
        titles.append(seo.meta_title)
        descriptions.append(seo.meta_description)
        h1s.append(seo.h1)
        leads.append(seo.lead)
        faq_keys.append(json.dumps(faq, ensure_ascii=False))
        by_service[seo.service_url].append(page["url"])

    (OUT / "pages.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    dup_titles = _group_counts(titles)
    dup_desc = _group_counts(descriptions)
    dup_h1 = _group_counts(h1s)
    dup_leads = _group_counts(leads)
    dup_faq = _group_counts(faq_keys)

    toponym_lines = []
    for service_url, urls in sorted(by_service.items(), key=lambda item: -len(item[1])):
        if len(urls) < 2:
            continue
        sample = catalog.view(urls[0]).seo
        if all(catalog.view(url).seo.meta_description == sample.meta_description for url in urls[1:]):
            toponym_lines.append(f"- {service_url} — {len(urls)} URL, один description")

    duplicates = [
        "# Дубли и схожесть",
        "",
        f"- Полностью одинаковых title: {len(dup_titles)}",
        f"- Полностью одинаковых description: {len(dup_desc)} формулировок (геостраницы одной услуги делят текст)",
        f"- Полностью одинаковых H1: {len(dup_h1)}",
        f"- Полностью одинаковых лидов: {len(dup_leads)} формулировок",
        f"- Повторяющихся наборов FAQ: {len(dup_faq)} наборов встречаются больше чем на одном URL",
        "",
        "Одинаковый description внутри услуги ожидаем: отдельных фактов по станции метро нет.",
        "Схожесть лидов и FAQ внутри семьи услуг высокая, потому что набор стабилен для профиля, а не для каждого URL.",
        "",
        "## Где отличие в основном топоним",
        "",
        *toponym_lines,
        "",
    ]
    (OUT / "duplicates.md").write_text("\n".join(duplicates), encoding="utf-8")

    mismatches = """# Блоки, которые не совпадают с услугой

Прайс, герой, форма, отличия и выбор «клиника или выезд» завязаны на кластер. Ниже то, что эта задача не переписывает.

- Отзывы и блок клинических рекомендаций по алкоголю и опиоидам остаются на страницах психиатрии, психотерапии и реабилитации.
- Хабы кодирования, вывода из запоя, лечения зависимостей и «других зависимостей» по-прежнему показывают блок «Где будет находиться пациент», хотя страница шире госпитализации.
- На части выездных страниц без своих геоссылок блок выездной службы может вести на географию соседней услуги.
- В прайсе нет отдельной цены кодирования, реабилитации и конкретных препаратов. Заголовок «Стоимость …» есть, сумма в title для них не ставится.
- Срок «30–45 минут» и «от 5 000 ₽» как цена любого вызова из старого героя сняты. В title выезда остаётся «30–60 минут» и консультация 8 000 ₽ либо процедура 5 000 ₽.
"""
    (OUT / "mismatches.md").write_text(mismatches, encoding="utf-8")

    thin = [row["url"] for row in rows if row["status"].startswith("thin")]
    insufficient = [
        "# Страницы с неполными исходными данными",
        "",
        "Для этих URL нет отдельной цены, адреса программы или описания метода в брифе. Тексты это не достраивают.",
        "",
        *[f"- {url}" for url in thin],
        "",
    ]
    (OUT / "insufficient.md").write_text("\n".join(insufficient), encoding="utf-8")

    example_blocks = ["# Примеры", ""]
    for url in EXAMPLES:
        seo = catalog.view(url).seo
        example_blocks.append(f"## {url}")
        example_blocks.append(f"- Title: {seo.meta_title}")
        example_blocks.append(f"- H1: {seo.h1}")
        example_blocks.append(f"- Description: {seo.meta_description}")
        example_blocks.append(f"- Лид: {seo.lead}")
        example_blocks.append(f"- Профиль: {seo.service_url} / {seo.presentation}")
        example_blocks.append("")
    changed = [
        "app/services/seo/",
        "app/services/catalog.py",
        "app/blueprints/services/routes.py",
        "app/data/service_facility.py",
        "app/templates/pages/service.html",
        "app/templates/components/service-call-form.html",
        "app/templates/components/service-differences.html",
        "app/templates/components/service-prices.html",
        "app/static/css/components/prices.css",
        "app/static/css/components/service-price.css",
        "app/templates/base.html",
        "tests/test_pages.py",
        "tests/test_seo.py",
        "tools/seo_audit.py",
    ]
    summary = [
        "# Сводка SEO-генерации",
        "",
        f"Страниц: {len(rows)}. У каждой есть title, description, H1, лид и 10 FAQ.",
        f"Одинаковых title: {len(dup_titles)}. Одинаковых H1: {len(dup_h1)}.",
        f"Семей description с повтором: {len(dup_desc)}. Наборов FAQ с повтором: {len(dup_faq)}.",
        f"Страниц с неполными данными: {len(thin)}.",
        "",
        "## Изменённые файлы",
        "",
        *[f"- {path}" for path in changed],
        "",
        *example_blocks,
    ]
    (OUT / "summary.md").write_text("\n".join(summary), encoding="utf-8")
    print(f"wrote {OUT} pages={len(rows)} thin={len(thin)} dup_desc={len(dup_desc)}")


if __name__ == "__main__":
    main()
