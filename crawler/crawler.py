import scrapping
import pickle
import os
import json
import concurrent.futures
import time

baseUrl = "https://www.ifsudestemg.edu.br/editais/editais-de-barbacena"

perPage = 30
currentPage = 0
links = []
notices = []
FILENAME = "../notices/notices.pickle"

startTime = time.time()

while True:
    resp = scrapping.get_links(f'{baseUrl}/?b_start:int={currentPage}')
    currentPage += perPage
    if not resp:
        break
    links += resp


def get_notice_data(link):
    return scrapping.get_notice_data(link)


with concurrent.futures.ThreadPoolExecutor() as executor:
    notices = list(executor.map(get_notice_data, links))

endTime = time.time()
responseTime = (endTime - startTime) * 1000
print(f"Tempo de resposta: {responseTime:.0f}ms\n")

os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
with open(FILENAME, 'wb') as f:
    pickle.dump(json.dumps(notices), f)
