# -*- coding: utf-8 -*-
"""Обратный чек-лист для кандидата — Захаров Альберт. Полный список навыков из схемы 5 недель."""
from pathlib import Path
import html
import shutil

OUT = Path(__file__).resolve().parent / "index.html"
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def esc(s):
    return html.escape(s, quote=True)


def field(label, value=""):
    val = f' value="{esc(value)}"' if value else ""
    return f"""
    <label class="field">
      <span>{esc(label)}</span>
      <input type="text" data-k class="ink" autocomplete="off"{val} />
    </label>"""


def skill_row(text):
    return f"""
    <div class="row">
      <div class="row-text">{esc(text)}</div>
      <label class="pick"><input type="radio" name="{esc(text)[:40]}" data-k value="know" /><span>Знаю</span></label>
      <label class="pick"><input type="radio" name="{esc(text)[:40]}" data-k value="got" /><span>Понял</span></label>
      <label class="pick"><input type="radio" name="{esc(text)[:40]}" data-k value="skip" /><span>Не успели</span></label>
      <label class="pick"><input type="radio" name="{esc(text)[:40]}" data-k value="unclear" /><span>Неясно</span></label>
    </div>"""


def section(title, texts, note=""):
    note_html = f'<p class="when">{esc(note)}</p>' if note else ""
    rows = "\n".join(skill_row(t) for t in texts)
    return f"""
    <section class="block">
      <h2>{esc(title)}</h2>
      {note_html}
      <div class="head-row">
        <div class="row-text">Навык / тема</div>
        <span>Знаю</span><span>Понял</span><span>Не успели</span><span>Неясно</span>
      </div>
      {rows}
    </section>"""


# Полный список из схемы 5 недель (архив 5+1), без служебных «тест пройден»
week1 = [
    "Обойти склад и зону приёмки: маршруты, зоны хранения, брак, ворота",
    "Работа в 1С:Торговля по складским операциям: остаток, карточка, документы",
    "Работа с ТСД на складе",
    "Приёмка с РЦ",
    "Приёмка от поставщиков",
    "Перемещения между магазинами под клиентов",
    "Подготовка товара к перемещению на РЦ или по заявке ИМ",
    "Сборка автозаказов",
    "Сборка и выдача заказов интернет-магазина",
    "Пересчёты и задания от ревизионного отдела",
    "Работа с браком: куда класть, как учитывать, кого привлекать",
    "Работа с отрицательными остатками",
    "Закрытие дня склада: 1С проведено, ТСД закрыт, ворота на ключ",
    "Самостоятельно принять машину (приёмка без подсказок)",
]

week2 = [
    "Открытие и закрытие смены на кассе",
    "Проверка расходников и связь с эквайринговым терминалом",
    "Продажа наличными и картой; сдача и оформление чека",
    "Возврат своего магазина и порядок возврата из другого магазина сети",
    "Размен и вечерний кассовый отчёт",
    "Работа с подарочным сертификатом, скидками и промокодами",
    "Работа с весовым товаром и весами",
    "Работа и продажи на КСО",
    "Допродажи на кассе: сопутка, увеличение чека",
    "Печать и замена ценников; работа с акциями на кассе и в зале рядом с кассой",
    "Действия при ошибке терминала и типовых сбоях кассы",
]

week3 = [
    "Продажа: встреча, потребность, оффер 2–3, закрытие",
    "Допродажи и предложение сопутствующего товара",
    "Доп. сервисы: доставка, погрузка, под заказ, помощь донести до машины",
    "Работа в 1С: поиск товара в Помощнике продаж, остаток, наличие по телефону только после проверки",
    "Что ещё делает ПК помимо продаж: выкладка, ценники, чистота зоны, помощь складу и кассе",
    "Утренняя выкатка, порядок на улице и вечерняя закатка товара",
    "Сборка техники вместе с РТЗ на примере одной позиции",
    "Работа с лояльностью: QR / бонусы",
    "Аналитика своих чеков за день",
]

week4 = [
    "Карточка корпоративного клиента и условия работы",
    "Оформление заказа и реализации для юрлица",
    "Проверка доверенности и комплекта документов на отгрузку",
    "Выписка УПД и контроль подписания",
    "Работа в ЭДО",
    "Документооборот магазина по корпоративным отгрузкам и оплатам",
    "Типичные вопросы и возражения корпоративного клиента",
    "Связка МОП — склад — касса: кто что делает на отгрузке",
]

week5 = [
    "Управление командой: пятиминутка, постановка задач, контроль исполнения",
    "Обход точки и фиксация замечаний с исполнителями и сроком",
    "Работа с отчётами и задачами в Битрикс24",
    "Работа с отчётами в 1С: ТО, план/факт, неликвиды, мотивация сотрудников",
    "Контроль состояния магазина: товар в зале, ценники, чистота, внешний вид смены",
    "Мин-максы, пустые крючки и «извиняшки»",
    "Контроль кассира, продавца, РТЗ и кладовщика в течение смены",
    "Кому звонить в нештатных ситуациях",
    "Полный день управления командой: планерки, чек-листы, задачи, состояние магазина",
]

# unique radio names - skill_row uses truncated name which could collide
# Fix: use index-based names instead


def skill_row_i(i, text):
    name = f"s{i}"
    return f"""
    <div class="row">
      <div class="row-text">{esc(text)}</div>
      <label class="pick"><input type="radio" name="{name}" data-k value="know" /><span>Знаю</span></label>
      <label class="pick"><input type="radio" name="{name}" data-k value="got" /><span>Понял</span></label>
      <label class="pick"><input type="radio" name="{name}" data-k value="skip" /><span>Не успели</span></label>
      <label class="pick"><input type="radio" name="{name}" data-k value="unclear" /><span>Неясно</span></label>
    </div>"""


def section_i(title, texts, start_i, note=""):
    note_html = f'<p class="when">{esc(note)}</p>' if note else ""
    rows = []
    i = start_i
    for t in texts:
        rows.append(skill_row_i(i, t))
        i += 1
    return "".join(rows), i, f"""
    <section class="block">
      <h2>{esc(title)}</h2>
      {note_html}
      <div class="head-row">
        <div class="row-text">Навык / тема</div>
        <span>Знаю</span><span>Понял</span><span>Не успели</span><span>Неясно</span>
      </div>
      {''.join(rows)}
    </section>"""


parts = []
idx = 0
for title, texts, note in [
    ("1. Кладовщик", week1, "Из полной программы 5 недель"),
    ("2. Кассир", week2, "Из полной программы 5 недель"),
    ("3. Продавец-консультант", week3, "Из полной программы 5 недель"),
    ("4. МОП", week4, "Из полной программы 5 недель"),
    ("5. СПК", week5, "Из полной программы 5 недель"),
]:
    _rows, idx, html_sec = section_i(title, texts, idx, note)
    parts.append(html_sec)

sections_html = "".join(parts)

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Обратный чек-лист — Захаров Альберт — Академия УМ</title>
  <meta name="description" content="Самооценка кандидата после стажировки: знаю / понял / не успели / неясно. Захаров Альберт, СПК Успенка, 17–20.11.2026." />
  <meta name="theme-color" content="#222222" />
  <style>
    :root {{
      --ink: #222;
      --paper: #fff;
      --page-w: 210mm;
      --font: Arial, "Helvetica Neue", Helvetica, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      font-family: var(--font);
      font-size: 14px;
      line-height: 1.4;
      background: #f0f0f0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .toolbar {{
      position: sticky; top: 0; z-index: 50;
      display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      background: #555; color: #fff; font-size: 12px;
    }}
    .toolbar .brand {{ display: flex; align-items: center; gap: 8px; }}
    .toolbar .brand img {{
      height: 28px; background: #fff; padding: 2px 4px;
      filter: grayscale(1) opacity(0.85);
    }}
    .toolbar .actions {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }}
    .toolbar button {{
      border: 1px solid #ccc; background: transparent; color: #fff;
      font: inherit; font-size: 12px; padding: 5px 10px; cursor: pointer;
    }}
    .toolbar button.primary {{ background: #fff; color: #444; border-color: #fff; }}
    .toolbar .status {{ font-size: 11px; opacity: .85; }}
    .sheet-wrap {{ width: min(var(--page-w), calc(100% - 16px)); margin: 12px auto 32px; }}
    .sheet {{
      background: var(--paper);
      border: 1px solid #bbb;
      box-shadow: 0 1px 6px rgba(0,0,0,.08);
      padding: 16px 14px 22px;
    }}
    .motto {{ text-align: center; color: #888; font-size: 12px; margin: 0 0 8px; letter-spacing: .04em; }}
    .title-block {{
      text-align: center; margin: 0 0 12px; padding: 0 0 10px; border-bottom: 1px solid #ccc;
    }}
    .title-block .logo {{
      display: block; width: min(140px, 42%); height: auto; margin: 0 auto 6px;
      filter: grayscale(1) opacity(0.75);
    }}
    .eyebrow {{ margin: 0; font-size: 11px; color: #999; }}
    h1 {{ font-weight: 600; font-size: 17px; margin: 4px 0 2px; color: #555; }}
    .meta {{ display: grid; gap: 8px; margin: 0 0 12px; }}
    .field {{
      display: grid; grid-template-columns: 180px 1fr; gap: 8px;
      align-items: end; font-size: 14px;
    }}
    .field span {{ color: #444; }}
    .field .ink, .sign .ink {{
      border: none; border-bottom: 1px solid #999; background: transparent;
      font: inherit; font-size: 14px; padding: 2px 4px; width: 100%;
    }}
    .scheme {{ margin: 0 0 14px; font-size: 13px; color: #555; line-height: 1.45; }}
    .scheme b {{ color: #444; }}
    .legend {{
      display: flex; flex-wrap: wrap; gap: 8px 14px;
      margin: 0 0 14px; font-size: 12px; color: #555;
    }}
    .block {{ margin: 0 0 16px; }}
    h2 {{ font-weight: 600; font-size: 15px; color: #444; margin: 0 0 6px; }}
    .when {{ margin: 0 0 8px; font-size: 12px; color: #777; }}
    .head-row, .row {{
      display: grid;
      grid-template-columns: 1fr 52px 52px 64px 56px;
      gap: 4px;
      align-items: center;
      padding: 5px 0;
      border-bottom: 1px solid #eee;
    }}
    .head-row {{
      font-size: 11px; color: #666; font-weight: 600;
      border-bottom: 1px solid #ccc; padding-bottom: 6px; margin-bottom: 2px;
    }}
    .head-row span, .row .pick {{ text-align: center; }}
    .row-text {{ font-size: 13px; line-height: 1.35; padding-right: 4px; }}
    .pick {{
      display: flex; justify-content: center; align-items: center;
      cursor: pointer; font-size: 0;
    }}
    .pick span {{ display: none; }}
    .pick input {{ width: 15px; height: 15px; margin: 0; cursor: pointer; }}
    .admit {{
      margin: 18px 0 0; padding-top: 12px; border-top: 1px solid #ccc;
    }}
    .admit h2 {{ margin-bottom: 8px; }}
    .sign {{ display: grid; gap: 8px; margin-top: 10px; }}
    .sign .field {{ grid-template-columns: 160px 1fr; }}
    @media (max-width: 700px) {{
      .head-row, .row {{
        grid-template-columns: 1fr;
        gap: 6px;
      }}
      .head-row {{ display: none; }}
      .pick {{
        justify-content: flex-start; gap: 6px; font-size: 13px;
      }}
      .pick span {{ display: inline; color: #444; }}
      .field, .sign .field {{ grid-template-columns: 1fr; }}
    }}
    @media print {{
      .toolbar {{ display: none !important; }}
      body {{ background: #fff; font-size: 12px; }}
      .sheet-wrap {{ width: 100%; margin: 0; }}
      .sheet {{ border: none; box-shadow: none; padding: 0; }}
      .title-block .logo {{ width: 100px; opacity: .55; filter: grayscale(1); }}
      .row-text {{ font-size: 11px; }}
      .block {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <div class="toolbar">
    <div class="brand">
      <img src="assets/logo.png" alt="У Михалыча" width="120" height="36" />
      <span>Академия УМ · обратный чек-лист · Захаров</span>
    </div>
    <div class="actions">
      <span class="status" id="save-status">онлайн-сохранение в этом браузере</span>
      <button type="button" id="btn-save">Сохранить</button>
      <button type="button" id="btn-clear">Очистить</button>
      <button type="button" class="primary" id="btn-print">Печать / PDF</button>
    </div>
  </div>

  <div class="sheet-wrap">
    <article class="sheet" id="checklist">
      <p class="motto">Делаем мир крепче</p>
      <header class="title-block">
        <img class="logo" src="assets/logo.png" alt="У Михалыча" width="250" height="72" />
        <p class="eyebrow">Академия УМ · сеть «У Михалыча»</p>
        <h1>Обратный чек-лист · для кандидата</h1>
      </header>

      <div class="meta">
        {field("Стажёр", "Захаров Альберт")}
        {field("Должность", "СПК Успенка")}
        {field("Место стажировки", "Перевалово")}
        {field("Даты стажировки", "17.11.2026 · 18.11.2026 · 19.11.2026 · 20.11.2026")}
        {field("Наставник", "Суковатая Ольга, СПК Перевалово")}
      </div>

      <p class="scheme">
        <b>Заполняет кандидат</b> Захаров Альберт.<br />
        По каждому пункту полной программы 5 недель отметьте одно:
        <b>Знаю</b> — умею сам · <b>Понял</b> — разобрали, ещё нужна практика ·
        <b>Не успели</b> — за 4 дня не дошли · <b>Неясно</b> — совсем непонятно, нужно объяснение.
      </p>

      <div class="legend">
        <span>☐ Знаю</span>
        <span>☐ Понял</span>
        <span>☐ Не успели</span>
        <span>☐ Неясно</span>
      </div>

      {sections_html}

      <section class="admit">
        <h2>Комментарий кандидата</h2>
        {field("Что самое полезное за 4 дня")}
        {field("Что обязательно доучить в первую очередь")}
        {field("Вопросы, которые остались")}
        <div class="sign">
          {field("Подпись стажёра", "Захаров Альберт")}
          {field("Подпись наставника", "Суковатая Ольга")}
          {field("Дата", "20.11.2026")}
        </div>
      </section>
    </article>
  </div>

  <script>
  (function () {{
    const KEY = "um-academy-spk-zaharov-reverse-20261117";
    const root = document.getElementById("checklist");
    const status = document.getElementById("save-status");
    const fields = () => root.querySelectorAll("[data-k]");

    function assignIds() {{
      fields().forEach((el, i) => {{
        if (!el.dataset.id) el.dataset.id = "f" + i;
      }});
    }}

    function collect() {{
      const data = {{}};
      fields().forEach((el) => {{
        const id = el.dataset.id;
        if (el.type === "radio") {{
          if (el.checked) data[id] = el.value;
        }} else if (el.type === "checkbox") {{
          data[id] = el.checked;
        }} else {{
          data[id] = el.value;
        }}
      }});
      // also store selected radio by name
      root.querySelectorAll('input[type="radio"]:checked').forEach((el) => {{
        data["n:" + el.name] = el.value;
      }});
      return data;
    }}

    function apply(data) {{
      if (!data) return;
      fields().forEach((el) => {{
        const id = el.dataset.id;
        if (el.type === "radio") {{
          const byName = data["n:" + el.name];
          if (byName) el.checked = el.value === byName;
          else if (id in data) el.checked = data[id] === el.value;
        }} else if (el.type === "checkbox") {{
          if (id in data) el.checked = !!data[id];
        }} else if (id in data && data[id]) {{
          el.value = data[id];
        }}
      }});
    }}

    function save(manual) {{
      try {{
        localStorage.setItem(KEY, JSON.stringify(collect()));
        const t = new Date();
        status.textContent = (manual ? "сохранено " : "автосохранение ") +
          t.toLocaleTimeString("ru-RU", {{ hour: "2-digit", minute: "2-digit" }});
      }} catch (e) {{
        status.textContent = "не удалось сохранить";
      }}
    }}

    function load() {{
      try {{
        const raw = localStorage.getItem(KEY);
        if (raw) apply(JSON.parse(raw));
      }} catch (e) {{}}
    }}

    assignIds();
    load();

    let timer;
    root.addEventListener("input", () => {{
      clearTimeout(timer);
      timer = setTimeout(() => save(false), 400);
    }});
    root.addEventListener("change", () => save(false));
    document.getElementById("btn-save").addEventListener("click", () => save(true));
    document.getElementById("btn-print").addEventListener("click", () => {{
      save(true);
      window.print();
    }});
    document.getElementById("btn-clear").addEventListener("click", () => {{
      if (!confirm("Очистить отметки в этом браузере?")) return;
      fields().forEach((el) => {{
        if (el.type === "radio" || el.type === "checkbox") el.checked = false;
        else if (el.defaultValue) el.value = el.defaultValue;
        else el.value = "";
      }});
      localStorage.removeItem(KEY);
      status.textContent = "очищено";
    }});
  }})();
  </script>
</body>
</html>
"""

OUT.write_text(doc, encoding="utf-8")
assets_out = Path(__file__).resolve().parent / "assets"
assets_out.mkdir(exist_ok=True)
if (ASSETS / "logo.png").exists():
    shutil.copy2(ASSETS / "logo.png", assets_out / "logo.png")
print("OK", OUT, OUT.stat().st_size)
