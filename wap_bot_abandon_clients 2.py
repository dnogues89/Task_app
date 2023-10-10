import requests
import schedule
from schedule import every,repeat
import time

@repeat(every(5).minutes)
def refresh_api():
    response = requests.get('http://daerwidd.pythonanywhere.com/abandon')
    if response.status_code == 200:
        if len(response.text)!=3:
            print(response.text)
            print(type(response.text))
            print(len(response.text))

    else:
        print("Error conectar")

refresh_api()

while True:
    schedule.run_pending()
    time.sleep(1)
