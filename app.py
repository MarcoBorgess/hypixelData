import itemUpdater as item
import bzUpdater as bz
import ahUpdater as ah
import datetime
from time import sleep

COOLDOWN = 900 # in seconds

last_week = 0

while True:
    now = datetime.datetime.now()
    week = now.strftime('%U')
    hour = now.strftime('%H')
    
    bz.updateBz()
    ah.updateAh()
    
    if (week > last_week):
        print('⌛ Updating items...')
        item.updateItemTable()
        last_week = week
    
    print(f'💤 NOW SLEEPING ({COOLDOWN}s) 💤')
    sleep(COOLDOWN)