import requests
from bs4 import BeautifulSoup

url = "https://nashville.granicus.com/player/camera/9?publish_id=32&redirect=true"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
current_agenda_item = soup.find(id="current-agenda-item")
print(current_agenda_item.text.strip())
