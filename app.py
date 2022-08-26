import itemUpdater as item
import bzUpdater as bz
import ahUpdater as ah
from time import sleep
from datetime import date

today = date.today().strftime('%d')
lastDay = 0

while True:
    # bz.updateBz()
    # ah.updateAh()
    
    if (today != lastDay):
        print('⌛ Updating items table, gonna take a while...')
        item.updateItemTable()
        lastDay = today
        
    print('💤 NOW SLEEPING 💤')
    sleep(300)