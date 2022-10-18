from Crypto.Util.number import getPrime, isPrime

p = 2
while True:
    p *= getPrime(20)
    if p.bit_length() == 1024:
        print(p)
        if isPrime( p + 1 ):
            print( p + 1 )
            break
        else:
            p = 2
            continue

    if p.bit_length() > 1024:
        p = 2
