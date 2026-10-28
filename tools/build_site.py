#!/usr/bin/env python3
"""Собирает HTML страницы сайта из общих частей. Запуск из корня репозитория: python3 tools/build_site.py"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from partials import head, nav, FOOT

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
names = open(f'{root}/names.js', encoding='utf8').read()
CL = json.loads(re.search(r'var CL=(\[.*?\]);', names, re.S).group(1))
CNT = json.loads(re.search(r'var CNT=(\{.*?\});', names).group(1))
TOTAL = sum(CNT.values())
docs = open(f'{root}/data/docs.js', encoding='utf8').read()
DOC_TITLES = [t.split(':')[0] if len(t) > 90 else t for t in re.findall(r'"md": "# ([^\\]+)', docs)]
BLURB = {
    'Здоровье и выживание': 'Давление, прививки, курение, экстренные ситуации и домашняя аптечка',
    'Силы, время, отдых': 'Сон, внимание, привычки и способы отдохнуть так, чтобы это помогало',
    'Деньги и быт': 'Кредиты, страховки, подписки, жильё и безопасность аккаунтов',
    'Закон и свобода': 'ДТП, мошенники, долги и красные линии, о которых нужно знать',
    'Работа и дело': 'Увольнение, отпуск, свой бизнес и учёба, которая окупается',
    'Семья': 'Брак, беременность, дети и пожилые родные',
    'За границей': 'Поездки и документы за рубежом',
    'Тяжёлые удары и инвалидность': 'Утрата, тяжёлый диагноз и жизнь после инвалидности',
}

def write(name, html):
    open(f'{root}/{name}', 'w', encoding='utf8').write(html)

FAQ = [
 ('Это медицинская или юридическая консультация?',
  'Нет. Справочник помогает сориентироваться и задать врачу или юристу правильные вопросы. Решения о здоровье, деньгах и праве принимайте с профильным специалистом и по актуальной редакции закона.'),
 ('Откуда взяты советы?',
  'Это русская версия китайского справочника «高性价比人生指南» (проект eternity4719/HowToLiveBetter на GitHub, лицензия CC BY 4.0). В оригинале у каждого совета есть оценка затрат, польза, класс доказательности и ссылки на исследования и официальные документы.'),
 ('Почему советов 512, а не 765?',
  'Из 765 исходных советов 134 универсальны и оставлены как есть. Ещё 378 касались китайских норм и переписаны под российские реалии. 253 совета описывали китайскую специфику без российского аналога, поэтому их убрали.'),
 ('Как проверялись российские нормы?',
  'Перевод и адаптацию сделал ИИ без редактора носителя языка. Для каждого адаптированного совета нормы искались по открытым российским источникам, затем второй проход независимо перепроверял суммы, сроки и ссылки. Исправлено 190 советов из 378. Что подтвердить не удалось, помечено словами «Проверьте актуальную норму». Ошибки всё равно возможны.'),
 ('Что значат классы A, B и C?',
  'A: есть конкретное число из метаанализа, большого наблюдения или рандомизированного испытания. B: исследования есть, но точного числа нет. C: опыт автора или общее мнение. Класс показан у универсальных советов, у адаптированных стоит пометка «Адаптировано для РФ» и список источников.'),
 ('Где хранится избранное?',
  'Только в браузере на вашем устройстве. Сайт не отправляет список на сервер и не требует регистрации. Если очистить данные сайта, избранное пропадёт, поэтому список можно скопировать текстом.'),
 ('Это бесплатно?',
  'Да. Без регистрации, подписки и рекламы.'),
 ('Как сообщить об ошибке или устаревшей норме?',
  'Откройте обращение на GitHub: github.com/VisualDrug/special-waffle/issues. Укажите номер совета в формате «раздел.совет» и что именно устарело.'),
 ('Можно ли использовать тексты?',
  'Да, на условиях CC BY 4.0: укажите оригинал «高性价比人生指南» (eternity4719), приложите ссылку на лицензию и отметьте, что текст изменён.'),
]

def faq_html():
    items = ''.join(f'<details><summary><span>{q}</span><i class="ph ph-caret-down" aria-hidden="true"></i></summary><div class="a">{a}</div></details>' for q, a in FAQ)
    return items

def faq_schema():
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}, ensure_ascii=False)

# ---------- landing ----------
def landing():
    topics = ''
    for g, chs in CL:
        tot = sum(CNT[str(c)] for c in chs)
        topics += f'<a class="topic reveal" href="guide.html#s{chs[0]}"><b>{g}</b><span>{BLURB.get(g, "")}</span><span class="t-sm" style="color:var(--accent);font-weight:600">{tot} советов</span></a>'
    arts = ''.join(f'<a class="topic reveal" href="guide.html#d{i+1}"><b>{t}</b><span>Длинная статья с шагами, сроками и ссылками на законы</span></a>' for i, t in enumerate(DOC_TITLES))
    h = head('Искусство жить: 512 советов для жизни в России',
             'Справочник советов о здоровье, деньгах, работе и семье для России. У каждого совета указано, сколько он стоит и что даёт, и насколько это доказано.',
             '', extra=f'<script type="application/ld+json">{faq_schema()}</script>')
    body = f'''<body>
{nav('home')}
<main id="main">
<section class="hero"><div class="container hero-grid">
  <div class="stack g-300">
    <span class="eyebrow">Справочник советов для жизни в России</span>
    <h1>Меньше лишних трат и рисков, больше спокойных лет</h1>
    <p class="lead">{TOTAL} советов о здоровье, деньгах, работе и семье. У каждого сказано, сколько он стоит в деньгах, времени и силе воли, что вы получите взамен и насколько это доказано.</p>
    <div class="stack g-100" style="align-items:flex-start">
      <a class="btn" href="cards.html">Вытянуть первую карту <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
      <span class="hero-note">Бесплатно, без регистрации и без рекламы</span>
    </div>
    <p class="proof"><span><b>{TOTAL}</b> советов</span><span><b>31</b> раздел</span><span><b>378</b> адаптированы под российские нормы</span></p>
  </div>
  <div class="card sample" aria-label="Пример карточки из справочника">
    <div class="chap">Раздел 1 · Не умереть раньше времени · совет 7</div>
    <h2 style="font-size:20px;line-height:28px">Измеряйте давление и, если оно повышено, идите к врачу и снижайте его до целевого уровня</h2>
    <p>Каждые 10 мм рт. ст. снижения верхнего давления уменьшают риск крупных болезней сердца и сосудов на 20%, инсульта на 27%, смерти на 13%.</p>
    <p class="cost"><b>Недорого · Быстро · Немного воли.</b> Домашний тонометр покупается один раз, измерение занимает минуту. Принимать лекарства нужно и без симптомов.</p>
    <div class="tags"><span class="tag L">Жизнь</span><span class="tag">Доказательность A</span><span class="tag top">Очень выгодно</span></div>
  </div>
</div></section>

<section class="section" aria-label="Главная мысль"><div class="container">
  <p class="tagline" data-tagline>Не нужно менять жизнь целиком. Достаточно выбрать одну вещь, которая бережёт здоровье или деньги, и сделать её сегодня.</p>
</div></section>

<section class="section" id="problem"><div class="container stack g-600">
  <div class="stack g-100 reveal"><span class="eyebrow">Зачем это нужно</span><h2 class="h" style="max-width:680px">Советов в сети много. Цену и доказательства видно редко.</h2></div>
  <div class="two">
    <div class="card reveal"><h3 class="h">Как обычно</h3>
      <ul class="stack g-75" style="margin:0;padding-left:24px"><li>Обещают результат и молчат о цене.</li><li>Не отличают исследование от чужого мнения.</li><li>Нормы давно устарели, а ссылок нет.</li></ul></div>
    <div class="card reveal"><h3 class="h">Как здесь</h3>
      <ul class="stack g-75" style="margin:0;padding-left:24px"><li>У каждого совета три оси затрат: деньги, время, сила воли.</li><li>Класс доказательности A, B или C и ссылки на источники.</li><li>Для российских норм указаны статья закона и первоисточник.</li></ul></div>
  </div>
</div></section>

<section class="section" id="benefits"><div class="container stack g-600">
  <div class="stack g-100 reveal"><span class="eyebrow">Что внутри</span><h2 class="h" style="max-width:680px">Каждый совет можно взвесить за минуту</h2></div>
  <div class="grid4">
    <div class="feature reveal"><i class="ph ph-coins" aria-hidden="true"></i><h3>Цена видна заранее</h3><p>Метки «Бесплатно», «Быстро», «Без усилий воли» показывают, во что обойдётся совет, ещё до чтения.</p></div>
    <div class="feature reveal"><i class="ph ph-flask" aria-hidden="true"></i><h3>Доказательность по шкале</h3><p>Класс A означает число из метаанализа или крупного исследования. Класс C означает опыт автора.</p></div>
    <div class="feature reveal"><i class="ph ph-scales" aria-hidden="true"></i><h3>Нормы для России</h3><p>378 советов переписаны под ТК РФ, ОМС, Госуслуги, ОСАГО и другие российские правила, с ссылками на первоисточники.</p></div>
    <div class="feature reveal"><i class="ph ph-cards" aria-hidden="true"></i><h3>Колода и избранное</h3><p>Тяните случайные карточки по одной или тремя сразу, сохраняйте нужное и копируйте список текстом.</p></div>
  </div>
</div></section>

<section class="section" id="how"><div class="container stack g-600">
  <div class="stack g-100 reveal"><span class="eyebrow">Как это работает</span><h2 class="h">Три шага от карточки до дела</h2></div>
  <div class="steps">
    <div class="step reveal"><span class="n">Шаг 1</span><h3 class="h">Вытяните карту</h3><p class="muted">Возьмите случайный совет или отфильтруйте колоду: жизнь, время, деньги, свобода, только бесплатные.</p></div>
    <div class="step reveal"><span class="n">Шаг 2</span><h3 class="h">Оцените цену и пользу</h3><p class="muted">Прочитайте затраты, ожидаемый результат и класс доказательности. Раскройте источники, если хотите проверить.</p></div>
    <div class="step reveal"><span class="n">Шаг 3</span><h3 class="h">Сохраните нужное</h3><p class="muted">Добавьте совет в избранное, скопируйте ссылку на карточку или весь список и сделайте первый шаг сегодня.</p></div>
  </div>
</div></section>

<section class="section" id="proof"><div class="container stack g-600">
  <div class="stack g-100 reveal"><span class="eyebrow">Из чего сделан справочник</span><h2 class="h" style="max-width:680px">Числа, которые можно проверить</h2></div>
  <div class="stats reveal">
    <div class="stat"><b>765</b><span>советов в китайском оригинале</span></div>
    <div class="stat"><b>134</b><span>универсальных оставлено без изменений</span></div>
    <div class="stat"><b>378</b><span>переписаны под российские нормы</span></div>
    <div class="stat"><b>2508</b><span>ссылок на первоисточники в оригинале</span></div>
  </div>
  <p class="muted reveal" style="max-width:680px">Российские нормы искали по открытым источникам, а затем независимо перепроверяли. На втором проходе исправлено 190 из 378 адаптированных советов. Что не подтвердилось, помечено «Проверьте актуальную норму».</p>
</div></section>

<section class="section" id="topics"><div class="container stack g-600">
  <div class="stack g-100 reveal"><span class="eyebrow">Темы</span><h2 class="h">Выберите область жизни</h2></div>
  <div class="grid3">{topics}</div>
</div></section>

<section class="section" id="articles"><div class="container stack g-600">
  <div class="stack g-100 reveal"><span class="eyebrow">Длинные статьи</span><h2 class="h" style="max-width:680px">Девять ситуаций, которые стоит разобрать подробно</h2></div>
  <div class="grid3">{arts}</div>
</div></section>

<section class="section faq" id="faq"><div class="container stack g-600">
  <div class="stack g-100 reveal"><span class="eyebrow">Вопросы</span><h2 class="h">Частые вопросы</h2></div>
  <div class="reveal" style="max-width:800px">{faq_html()}</div>
</div></section>

<section class="section" id="start"><div class="container">
  <div class="cta reveal">
    <span class="eyebrow">Без риска</span>
    <h2 class="h">Бесплатно, без регистрации. Избранное остаётся только у вас.</h2>
    <p class="muted" style="max-width:680px">Нашли ошибку или устаревшую норму? Напишите на GitHub, исправим.</p>
    <a class="btn" href="cards.html">Вытянуть первую карту <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
  </div>
</div></section>
</main>
{FOOT}</body></html>'''
    write('index.html', h + body)

# ---------- guide ----------
def guide():
    h = head('Все советы: искусство жить', f'Полный список из {TOTAL} советов с поиском и фильтрами по ресурсу, доказательности и затратам.', 'guide.html')
    body = f'''<body>
{nav('guide')}
<main id="main"><div class="container page-top stack g-400" style="padding-bottom:96px">
  <header class="stack g-100"><h1 style="font-size:36px;line-height:40px">Все советы</h1>
  <p class="lead">{TOTAL} советов в 31 разделе. Откройте раздел или найдите совет по слову и отфильтруйте по тому, что хотите сберечь.</p></header>
  <section aria-label="Карта разделов" class="stack g-200"><h2 class="h">Разделы</h2><div class="map" id="map"></div></section>
  <section id="guide" class="stack g-200" aria-label="Список советов">
    <div class="toolbar" role="search">
      <input id="q" class="search" type="search" placeholder="Поиск по советам: зубы, залог, ожог" aria-label="Поиск по советам" autocomplete="off">
      <div class="frow"><span class="lab">Ресурс</span>
        <button class="chip" data-g="lens" data-v="死亡率" aria-pressed="false">Жизнь</button>
        <button class="chip" data-g="lens" data-v="时间" aria-pressed="false">Время и силы</button>
        <button class="chip" data-g="lens" data-v="金钱" aria-pressed="false">Деньги</button>
        <button class="chip" data-g="lens" data-v="自由" aria-pressed="false">Свобода</button></div>
      <div class="frow"><span class="lab">Доказательность</span>
        <button class="chip" data-g="grade" data-v="A" aria-pressed="false">A</button>
        <button class="chip" data-g="grade" data-v="B" aria-pressed="false">B</button>
        <button class="chip" data-g="grade" data-v="C" aria-pressed="false">C</button>
        <button class="chip" data-g="grade" data-v="РФ" aria-pressed="false">Адаптировано для РФ</button>
        <span class="lab" style="margin-left:8px">Ещё</span>
        <button class="chip" data-g="top" data-v="1" aria-pressed="false">Очень выгодно</button>
        <button class="chip" data-g="free" data-v="1" aria-pressed="false">Бесплатно</button>
        <button class="chip" data-g="dis" data-v="1" aria-pressed="false">Спорное</button>
        <button class="chip" id="reset" aria-pressed="false">Сбросить</button></div>
      <div class="count" id="count" aria-live="polite"></div>
    </div>
    <div id="chapters" class="stack g-75"></div>
  </section>
  <section class="stack g-200" aria-label="Длинные статьи"><h2 class="h">Длинные статьи</h2><div id="docs" class="stack g-75"></div></section>
  <p class="note" style="max-width:680px">Классы доказательности: A, B, C для универсальных советов. Адаптированные советы помечены «Адаптировано для РФ»: нормы проверяйте по актуальной редакции закона. Ссылки вида «раздел X, совет Y» ведут на советы исходной книги, часть которых убрана.</p>
</div></main>
{FOOT}
<script src="names.js"></script>
<script src="app.js?v=3"></script>
</body></html>'''
    write('guide.html', h + body)

# ---------- cards ----------
def cards():
    h = head('Колода: случайные карточки советов', f'Вытягивайте случайные карточки из {TOTAL} советов и сохраняйте нужные в избранное.', 'cards.html')
    body = f'''<body>
{nav('cards')}
<main id="main"><div class="container page-top stack g-300" style="max-width:720px;padding-bottom:96px">
  <header class="stack g-100"><h1 style="font-size:36px;line-height:40px">Колода советов</h1>
  <p class="lead">Нажмите на колоду, чтобы вытянуть случайный совет. Нужные сохраняйте в избранное.</p></header>
  <div class="tabs" role="tablist" aria-label="Режим">
    <button class="tab" role="tab" id="t-deck" aria-selected="true" type="button">Колода</button>
    <button class="tab" role="tab" id="t-fav" aria-selected="false" type="button">Избранное <span id="favn">0</span></button>
  </div>
  <section id="deck" class="stage" aria-labelledby="t-deck">
    <div class="frow" role="group" aria-label="Фильтр колоды">
      <button class="chip" data-r="all" aria-pressed="true" type="button">Все</button>
      <button class="chip" data-r="死亡率" aria-pressed="false" type="button">Жизнь</button>
      <button class="chip" data-r="时间" aria-pressed="false" type="button">Время и силы</button>
      <button class="chip" data-r="金钱" aria-pressed="false" type="button">Деньги</button>
      <button class="chip" data-r="自由" aria-pressed="false" type="button">Свобода</button>
      <button class="chip" id="free" aria-pressed="false" type="button">Только бесплатные</button>
    </div>
    <button class="pile" id="pile" type="button" aria-label="Вытянуть карту из колоды"><span class="back"></span><span class="back"></span><span class="back">?</span></button>
    <div id="out" class="spread" aria-live="polite"></div>
    <div class="row">
      <button class="btn" id="draw" type="button"><i class="ph ph-cards" aria-hidden="true"></i> Вытянуть карту</button>
      <button class="btn ghost" id="three" type="button">Расклад из трёх</button>
      <button class="btn ghost" id="prev" type="button" disabled><i class="ph ph-arrow-left" aria-hidden="true"></i> Назад</button>
    </div>
    <div class="meta"><span id="left"></span><button class="chip" id="shuffle" type="button"><i class="ph ph-shuffle" aria-hidden="true"></i> Перемешать заново</button></div>
  </section>
  <section id="favs" hidden aria-labelledby="t-fav" class="stack g-200">
    <div class="row"><button class="btn ghost" id="copy" type="button"><i class="ph ph-copy" aria-hidden="true"></i> Скопировать список</button><button class="btn ghost" id="clear" type="button">Очистить</button></div>
    <div id="favlist" class="spread"></div>
  </section>
  <p class="note">Избранное хранится только в вашем браузере на этом устройстве. Адаптированные советы помечены «Адаптировано для РФ»; право и цены меняются, поэтому перед решением сверяйтесь с актуальным законом, врачом или юристом.</p>
</div></main>
<div class="toast" id="toast" role="status"></div>
{FOOT}
<script src="names.js"></script>
<script src="data/cards.js"></script>
<script src="deck.js?v=3"></script>
</body></html>'''
    write('cards.html', h + body)

# ---------- prose pages ----------
def prose(name, title, desc, inner, path):
    h = head(title, desc, path)
    write(name, h + f'<body>\n{nav("")}\n<main id="main"><div class="container page-top" style="padding-bottom:96px"><article class="prose">{inner}<p><a class="btn ghost" href="index.html"><i class="ph ph-arrow-left" aria-hidden="true"></i> На главную</a></p></article></div></main>\n{FOOT}</body></html>')

def pages():
    prose('privacy.html', 'Политика конфиденциальности: искусство жить', 'Какие данные сайт хранит и кому их передаёт.', '''<h1>Политика конфиденциальности</h1>
<p class="muted">Редакция от 28 октября 2026 года.</p>
<h2>Что сайт собирает</h2><p>Ничего. На сайте нет регистрации, форм, аналитики, рекламы и cookie. Сервер сайта (GitHub Pages) не получает от вас ничего, кроме обычных технических записей о запросах, которые ведёт сам GitHub.</p>
<h2>Что хранится на вашем устройстве</h2><ul><li><b>Избранное</b>: список номеров советов в localStorage браузера. Ключ vygodnee-fav.</li><li><b>Тема оформления</b>: выбор светлой или тёмной темы. Ключ theme.</li></ul><p>Эти данные не покидают ваше устройство. Очистить их можно в настройках браузера или кнопкой «Очистить» в избранном.</p>
<h2>Внешние ресурсы</h2><p>Для отображения сайт загружает шрифт Manrope с Google Fonts и значки Phosphor с jsDelivr. Эти сервисы видят ваш IP адрес и данные браузера, как при любой загрузке файла. Ссылки на источники в советах ведут на сторонние сайты со своими политиками.</p>
<h2>Связь</h2><p>Вопросы и сообщения об ошибках: github.com/VisualDrug/special-waffle/issues.</p>''', 'privacy.html')
    prose('terms.html', 'Условия использования: искусство жить', 'Условия использования сайта и ограничение ответственности.', '''<h1>Условия использования</h1>
<p class="muted">Редакция от 28 октября 2026 года.</p>
<h2>Назначение</h2><p>Сайт публикует справочные материалы. Это не медицинская, юридическая, налоговая или финансовая консультация и не заменяет специалиста.</p>
<h2>Точность</h2><p>Перевод и адаптация выполнены с помощью ИИ без редактора носителя языка. Российские нормы проверялись по открытым источникам, но право, суммы и порядок действий меняются. Перед решением сверяйтесь с актуальной редакцией закона, врачом или юристом. Сайт предоставляется как есть, без гарантий, и его автор не отвечает за последствия использования материалов.</p>
<h2>Лицензия и авторство</h2><p>Материалы основаны на справочнике «高性价比人生指南» (eternity4719/HowToLiveBetter, github.com/eternity4719/HowToLiveBetter), лицензия <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>. Текст переведён, сокращён и адаптирован, то есть изменён. При повторном использовании указывайте оригинал, лицензию и факт изменений.</p>''', 'terms.html')
    h = head('Страница не найдена: искусство жить', 'Такой страницы нет.', '404.html', noindex=True, base='<base href="/special-waffle/">\n')
    write('404.html', h + f'<body>\n{nav("")}\n<main id="main"><div class="container page-top" style="padding-bottom:96px"><div class="stack g-300" style="max-width:680px"><span class="eyebrow">Ошибка 404</span><h1 style="font-size:36px;line-height:40px">Такой страницы нет</h1><p class="lead">Возможно, ссылка устарела. Вернитесь на главную или вытяните случайную карту.</p><div class="row"><a class="btn" href="index.html">На главную</a><a class="btn ghost" href="cards.html">Вытянуть карту</a></div></div></div></main>\n{FOOT}</body></html>')

landing(); guide(); cards(); pages()
print('built')
