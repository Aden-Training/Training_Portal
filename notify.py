import datetime

current = datetime.datetime.now()
renew = current.minute + 1
print(renew)

while(True):
    current = datetime.datetime.now()
    if current.minute == renew:
        print("Time to renew")
        break
