import itemUpdater as item
import bzUpdater as bz
import ahUpdater as ah
import imgUpdater as img
import datetime
from time import sleep

COOLDOWN = 300 # in seconds

now = datetime.datetime.now()
day = now.day
hour = now.strftime('%H')

last_day = 0
last_hour = 0

while True:
    bz.updateBz()
    ah.updateAh()
    
    if (hour != last_hour):
        print('⌛ Updating images...')
        img.update_icon64_column()
        last_hour = hour
    
    if (day != last_day):
        print('⌛ Updating items...')
        item.updateItemTable()
        last_day = day
    
    print(f'💤 NOW SLEEPING ({COOLDOWN}s) 💤')
    sleep(COOLDOWN)