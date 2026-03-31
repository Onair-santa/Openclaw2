from playwright.sync_api import sync_playwright

def get_digest():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Новости
        page.goto("https://www.gipsyteam.ru/news")
        page.wait_for_timeout(3000)
        
        elements = page.query_selector_all('a')
        news = []
        for e in elements:
            href = e.get_attribute('href')
            text = e.inner_text().strip()
            if href and '/news/' in href and len(text) > 20 and 'sort' not in href and 'page' not in href and '?' not in href:
                url = href if href.startswith('http') else 'https://www.gipsyteam.ru' + href
                if not any(n[0] == text for n in news):
                    news.append((text, url))
                if len(news) >= 6: break
        
        print("😊 Новости GipsyTeam\n")
        for text, url in news:
            print(f"🔹 {text}")
            print(f"└─ [Читать]({url})\n")
        
        # Форум
        page.goto("https://forum.gipsyteam.ru/")
        page.wait_for_timeout(3000)
        
        links = page.query_selector_all('a')
        forum_links = []
        for l in links:
            href = l.get_attribute('href')
            text = l.inner_text().strip()
            # Фильтруем технические элементы
            if href and 'viewtopic=' in href and len(text) > 15:
                # Более строгий фильтр мусора
                if any(bad in text for bad in ['Вчера,', 'Сегодня,', 'Автор:', 'Ответов:', 'ФОРУМ', 'НОВЫЙ БЛОГ', 'ИСПОЛНЕНИЕ МЕЧТЫ', '4 ЛИСТА', 'НЕ ЗРЯ']): continue
                
                url = href if href.startswith('http') else 'https://forum.gipsyteam.ru' + (href if href.startswith('/') else '/' + href)
                topic_id = href.split('viewtopic=')[1].split('&')[0]
                if not any(f[2] == topic_id for f in forum_links):
                    forum_links.append((text, url, topic_id))
                if len(forum_links) >= 10: break
        
        print("—\n\n💻 Форум GipsyTeam\n")
        for text, url, _ in forum_links:
            print(f"🔹 {text}")
            print(f"└─ [Читать]({url})\n")
        
        browser.close()

if __name__ == "__main__":
    get_digest()
