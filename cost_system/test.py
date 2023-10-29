from bs4 import BeautifulSoup
import requests

url = 'http://127.0.0.1:5555/components_inventory/av_details'
response = requests.post(url)
print(response.text)
