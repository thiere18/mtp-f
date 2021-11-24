import random
def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1
    
unique_sequence = uniqueid()
