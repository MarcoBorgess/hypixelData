import bazaarUpdater as bz
import binsUpdater as bins
import itemInfoUpdater as itemInfo
from time import sleep

while True:
    bz.updateBazaar()
    bins.updateBins()
    itemInfo.updateItemsInfo()
    print('NOW SLEEPING 💤')
    sleep(900)