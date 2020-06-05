import requests
import time
import random

for i in range(100):
    url = 'https://vis.vip.com/checkCode.php'
    response = requests.get(url)
    img = response.content
    with open(f'./check_code/{i}.jpg', 'wb') as f:
        f.write(img)
    time.sleep(random.randint(5, 12))
