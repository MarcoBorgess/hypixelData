import bazaarUpdater as bz
import binsUpdater as bins
import itemInfoUpdater as itemInfo
from time import sleep
from datetime import date

today = date.today().strftime('%d')
lastDay = 0

while True:
    bz.updateBazaar()
    bins.updateBins()
    if (today != lastDay):
        print('Updating items info, gonna take a while... ⌛')
        itemInfo.updateItemsInfo()
        lastDay = today
    print('NOW SLEEPING 💤')
    sleep(900)