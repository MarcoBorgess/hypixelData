import itemUpdater as item
import bzUpdater as bz
import ahUpdater as ah
import datetime
from time import sleep

COOLDOWN = 900 # in seconds

last_day = 0

while True:
    now = datetime.datetime.now()
    day = now.day
    hour = now.strftime('%H')
    
    bz.updateBz()
    ah.updateAh()
    
    if (day != last_day):
        print('⌛ Updating items...')
        item.updateItemTable()
        last_day = day
    
    print(f'💤 NOW SLEEPING ({COOLDOWN}s) 💤')
    sleep(COOLDOWN)