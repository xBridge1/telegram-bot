from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def fetch_epic_page_with_browser():
    options = Options()
    options.headless = True  # Run without opening a browser window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://store.epicgames.com/en-US/free-games"
    driver.get(url)
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "css-1myhtyb"))
    )   

    html = driver.page_source
    driver.quit()
    return html


def parse_free_games(html): 
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="css-1myhtyb")

    games = []
    for card in cards:
        title_el = card.find("span")
        link_el = card.find("a", href=True)
        date_el = card.find("span", string=lambda text: text and "Free Now" in text and "-" in text)

        if not title_el or not link_el:
         continue 

    date_strings = soup.find_all(string=lambda t: t and "Free Now" in t and "-" in t)
    for date in date_strings:
        print(f"[DEBUG] Free game ends at: {date.strip()}")

    title = title_el.text.strip()
    url = "https://store.epicgames.com" + link_el["href"]
    free_until = date_el.text.strip() if date_el else "Data Indisponivel"
    games.append((title, url, free_until))
    print(f"[DEBUG] Date element: {date_el}")
    return games



def format_games_message(games):
    if not games:
        return "🚫 Sem Jogos gratis no momento."

    message = "🆓 **Agora gratis na Epic Games Store**:\n\n"
    for title, url, free_until in games:
        message += (
            f"🔗 [View Game]({url})\n\n"
        )

    return message