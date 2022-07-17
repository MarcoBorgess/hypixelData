import bazaarUpdater as bz
from time import sleep

while True:
    bz.updateBazaar()
    sleep(900)