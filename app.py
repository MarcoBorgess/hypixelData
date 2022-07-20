import bazaarUpdater as bz
import binsUpdater as bins
from time import sleep

while True:
    bz.updateBazaar()
    bins.updateBins()
    print('NOW SLEEPING 💤')
    sleep(900)