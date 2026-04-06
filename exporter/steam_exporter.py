from prometheus_client import start_http_server, Gauge
import requests
from bs4 import BeautifulSoup
import time

# Metrics
api_status = Gauge('steam_api_up', 'Steam API status: 1=up, 0=down')
steam_top_players = Gauge('steam_top_players', 'Current players of top Steam games', ['game'])
steam_top1_players = Gauge('steam_top1_players', 'Current players of the top 1 Steam game', ['game'])
steam_total_players = Gauge('steam_total_players', 'Total players in top Steam games')

def fetch_top_steam_games(top_n=5):
    url = "https://steamcharts.com/top"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("Error HTTP:", response.status_code)
            api_status.set(0)
            return

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table tbody tr")
        total_players = 0

        for i, row in enumerate(rows[:top_n]):
            cols = row.find_all("td")
            name = cols[1].text.strip()
            players = int(cols[2].text.strip().replace(",", ""))

            steam_top_players.labels(game=name).set(players)
            total_players += players

            # Top 1 game progression
            if i == 0:
                steam_top1_players.labels(game=name).set(players)

        steam_total_players.set(total_players)
        api_status.set(1)
        print("Metrics updated successfully.")

    except Exception as e:
        print("Error fetching Steam data:", e)
        api_status.set(0)

if __name__ == "__main__":
    start_http_server(9300)
    while True:
        fetch_top_steam_games()
        time.sleep(30)  # scrape every 30 seconds
