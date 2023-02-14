import random

def random_invoice_number():
    randomnumber = random.randint(1000000000000000,9999999999999999)
    invoicenumber = 'CMSK' + str(randomnumber)
    print(invoicenumber)
    return str(invoicenumber)
