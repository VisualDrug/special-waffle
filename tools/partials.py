# Общие части страниц: голова, навигация, подвал. Страницы собираются командой python3 tools/build_site.py
SITE='https://visualdrug.github.io/special-waffle/'
FAV="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23131209'/%3E%3Crect x='17' y='14' width='30' height='38' rx='5' fill='%23B6F36B'/%3E%3C/svg%3E"
def head(title,desc,path='',noindex=False,extra='',base=''):
    og=SITE+'og.png'
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{base}<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Искусство жить">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAV}">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/fill/style.css">
<link rel="stylesheet" href="site.css?v=3">
{extra}
</head>
'''
def nav(cur=''):
    def a(href,label,key):
        return f'<a href="{href}"{" aria-current=\"page\"" if cur==key else ""}>{label}</a>'
    links=[('guide.html','Советы','guide'),('cards.html','Колода','cards'),('index.html#faq','Вопросы','faq')]
    d=''.join(a(h,l,k) for h,l,k in links)
    m=''.join(f'<a href="{h}">{l}</a>' for h,l,k in [('index.html','Главная','')]+links)
    return f'''<a class="skip" href="#main">Перейти к содержимому</a>
<header class="nav-wrap"><nav class="nav" aria-label="Основная навигация">
<a class="brand" href="index.html"{' aria-current="page"' if cur=='home' else ''}>Искусство жить</a>
<div class="links">{d}</div>
<a class="btn sm" href="cards.html" style="display:none" id="navcta">Вытянуть карту</a>
<button class="icon-btn" id="theme" type="button" aria-label="Сменить тему"></button>
<button class="icon-btn burger" id="burger" type="button" aria-label="Меню" aria-expanded="false" aria-controls="mmenu"><span></span><span></span></button>
</nav></header>
<div class="mmenu" id="mmenu" aria-hidden="true">{m}</div>
<style>@media (min-width:768px){{#navcta{{display:inline-flex!important}}}}</style>
'''
FOOT='''<footer class="site"><div class="container"><div class="row">
<div class="col"><b style="color:var(--fg)">Искусство жить</b>
<span>Справочник советов для жизни в России. Перевод и адаптация справочника «高性价比人生指南» (eternity4719/HowToLiveBetter), лицензия CC BY 4.0. Текст изменён: переведён, сокращён и адаптирован.</span></div>
<div class="links-row"><a href="guide.html">Все советы</a><a href="cards.html">Колода</a><a href="privacy.html">Политика конфиденциальности</a><a href="terms.html">Условия использования</a><a href="https://github.com/eternity4719/HowToLiveBetter" target="_blank" rel="noopener">Оригинал на GitHub</a><a href="https://github.com/VisualDrug/special-waffle/issues" target="_blank" rel="noopener">Сообщить об ошибке</a></div>
</div></div></footer>
<script src="site.js?v=3"></script>
'''
