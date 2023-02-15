import random

def random_invoice_number_credit():
    randomnumber = random.randint(10000000000000,99999999999999)
    invoicenumber = 'CRCMSK' + str(randomnumber)
    print(invoicenumber)
    return str(invoicenumber)

def random_invoice_number_qr():
    randomnumber = random.randint(10000000000000,99999999999999)
    invoicenumber = 'QRCMSK' + str(randomnumber)
    print(invoicenumber)
    return str(invoicenumber)
