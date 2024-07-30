import requests
from lxml import html
from discord_webhook import DiscordWebhook
import schedule
import time

# Configuration
WEBHOOK_URL = 'https://ptb.discord.com/api/webhooks/1267938980410687508/ZmF1N0EzT4cHDuBLnzwD5i3MXO_C1kPfLQnVb3VBj5AHC-pi2FnZtGkF0eF7jkxdQXI0'  # Replace with your Discord webhook URL
STEAMCHARTS_URL = 'https://steamcharts.com/app/252490'
PLAYER_XPATH = '//*[@id="app-heading"]/div[1]/span'

def fetch_player_count():
    try:
        response = requests.get(STEAMCHARTS_URL)
        response.raise_for_status()  # Ensure we notice bad responses
        tree = html.fromstring(response.content)

        # Extract player count using XPath
        player_count_element = tree.xpath(PLAYER_XPATH)
        if player_count_element:
            return player_count_element[0].text.strip()
        else:
            print("Player count element not found.")
            return None

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def send_to_discord(message):
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=message)
    response = webhook.execute()
    if response.status_code != 200:
        print(f"Failed to send webhook: {response.status_code} - {response.text}")

def job():
    player_count = fetch_player_count()
    if player_count:
        message = f"Current Rust player count: {player_count}"
        send_to_discord(message)

# Schedule the job every 5 minutes
schedule.every(0.10).minutes.do(job)

# Run the scheduler
if __name__ == "__main__":
    print("Starting Rust player tracker...")
    while True:
        schedule.run_pending()
        time.sleep(1)
