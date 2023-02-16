import json
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib import messages

# หน้า
from django.core.paginator import Paginator

# django auth
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# custom decorators
from .decorators import *
# custom random invoicenumber
from .randominvoicenumber import random_invoice_number_qr, random_invoice_number_credit


# ส่งemail
from newform_test import settings
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
#สร้างtokens
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
# dajngoเวอชั่นเก่าใช้force_textแต่เวอชั่น4ขึ้นใช้force_strแทน
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token

# encode/decode
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# uuid
import uuid
from django.core.files.base import ContentFile

# urllib
from urllib import request, parse
from urllib.request import urlopen

# requests
import requests

from django.views.decorators.csrf import csrf_exempt

# date
import datetime

# pillow
import PIL.Image as Image
import io
import base64

# import models&forms
from . models import *
from . forms import *

# custom message level
SIGNUPSUCCESS = 50

# Create your views here.

def home(request):
    allcourse = CourseModel.objects.all().order_by('order_number')

    context = {
        'allcourse':allcourse,
        # 'allregis':allregis,
        # 'arrayimage1':arrayimage1,
    }
    return render(request, 'app_general/home.html', context)

def classroom(request, coursecode):
    thiscourse = CourseModel.objects.get(id=coursecode)
    allclass = ClassroomModel.objects.filter(course=coursecode)

    context = {
            'allclass':allclass,
            'thiscourse':thiscourse,
    }

    try:
        today = datetime.date.today()
        for classroom in allclass:
            startregis = classroom.earlybird_date_start
            endregis = classroom.fullprice_date_end
            if today >= startregis and today <= endregis:
                classroom.is_active = True
                classroom.save()
            else:
                classroom.is_active = False
                classroom.save()

            allclass_active = ClassroomModel.objects.filter(course=coursecode, is_active=True)

            context = {
                'allclass':allclass,
                'thiscourse':thiscourse,
                'allclass_active':allclass_active,
            }
    except:
        pass

    return render(request, 'app_general/classroom.html', context)

def registerform(request, classcode):

    thisclass = ClassroomModel.objects.get(id=classcode)
    try:
        thisvoucher = VoucherModel.objects.get(classroom=classcode)
    except:
        thisvoucher = None
        pass

    nowprice = thisclass.get_now_price
    print(nowprice)

    regisform = RegisterForm()

    if request.method == 'POST':

        getemail = request.POST['email']
        gettitlenameother = request.POST['titlenameother']
        getname = request.POST['name']
        getlastname = request.POST['lastname']
        getphone = request.POST['phone']
        getjob = request.POST['job']

        gethaveaccout = request.POST['haveaccout']
        getoldaccout = request.POST['oldaccout']
        getreceipt = request.POST['receipt']

        #
        getindiname = request.POST['indiname']
        getindilastname = request.POST['indilastname']
        getinditaxid = request.POST['inditaxid']

        getindiaddress = request.POST['indiaddress']
        getindicity = request.POST['indicity']
        getindistate = request.POST['indistate']
        getindipostal = request.POST['indipostal']
        getindicountry = request.POST['indicountry']

        getindiaddress_send = request.POST['indiaddress_send']
        getindicity_send = request.POST['indicity_send']
        getindistate_send = request.POST['indistate_send']
        getindipostal_send = request.POST['indipostal_send']
        getindicountry_send = request.POST['indicountry_send']
        #

        #
        getorgname = request.POST['orgname']

        getorgaddress1 = request.POST['orgaddress1']
        getorgaddress2 = request.POST['orgaddress2']
        getorgcity = request.POST['orgcity']
        getorgstate = request.POST['orgstate']
        getorgpostal = request.POST['orgpostal']
        getorgcountry = request.POST['orgcountry']

        getorgaddress1_send = request.POST['orgaddress1_send']
        getorgaddress2_send = request.POST['orgaddress2_send']
        getorgcity_send = request.POST['orgcity_send']
        getorgstate_send = request.POST['orgstate_send']
        getorgpostal_send = request.POST['orgpostal_send']
        getorgcountry_send = request.POST['orgcountry_send']

        getorgtaxid = request.POST['orgtaxid']
        #

        gettaxwithholding = request.POST['taxwithholding']

        # getacctype = request.POST['acctype']
        getimageevidence = request.FILES.get('imageevidence')
        # getimageevidence_data = request.FILES['imageevidence'].file.read()
        
        # getpaymenttype = request.POST['paymenttype']

        # getpaywithvoucher = request.POST['paywithvoucher']
        getimagevoucherevidence = request.FILES.get('imagevoucherevidence')
        # getimagevoucherevidence_data = request.FILES['imagevoucherevidence'].file.read()

        getacceptall = request.POST['acceptall']

        print(
            # invoicenumber,

            getemail,
            gettitlenameother,
            getname, 
            getlastname, 
            getphone, 
            getjob, 

            gethaveaccout, 
            getoldaccout,
            getreceipt,

            #
            getindiname,
            getindilastname,
            getinditaxid,

            getindiaddress,
            getindicity,
            getindistate,
            getindipostal,
            getindicountry,

            getindiaddress_send,
            getindicity_send,
            getindistate_send,
            getindipostal_send,
            getindicountry_send,
            #

            #
            getorgname,
            getorgaddress1,
            getorgaddress2,
            getorgcity,
            getorgstate,
            getorgpostal,
            getorgcountry,

            getorgaddress1_send,
            getorgaddress2_send,
            getorgcity_send,
            getorgstate_send,
            getorgpostal_send,
            getorgcountry_send,

            getorgtaxid,
            #

            gettaxwithholding,

            # getacctype,
            getimageevidence,

            # getpaymenttype,

            # getpaywithvoucher,
            getimagevoucherevidence,

            getacceptall,
        )

        # print("CHECKIMAGE", getimageevidence_data, getimagevoucherevidence_data)
        
        # SAVE DATA
        try:
            # print("a")
            regisform = RegisterForm(request.POST)
            if regisform.is_valid():
                # print("a")
                regisform.save()
                getthisregis = regisform.save(commit=False)

                getthis_channel = getthisregis.channel
                getthis_titlename = getthisregis.titlename
                getthis_acctype = getthisregis.acctype
                getthis_receipt = getthisregis.receipt
                getthis_paymenttype = getthisregis.paymenttype
                getthis_paywithvoucher = getthisregis.paywithvoucher
                
                # generate invoice number (QR OR CR)
                if getthis_paymenttype == "เงินโอน":
                    invoicenumber = random_invoice_number_qr()
                    # check invoice number ซ้ำหรือไม่
                    while RegisterModel.objects.filter(invoice_number = invoicenumber):
                        invoicenumber = random_invoice_number_qr()

                elif getthis_paymenttype == "บัตรเครดิต":
                    invoicenumber = random_invoice_number_credit()
                    # check invoice number ซ้ำหรือไม่
                    while RegisterModel.objects.filter(invoice_number = invoicenumber):
                        invoicenumber = random_invoice_number_credit()

                elif getthis_paywithvoucher == "เงินโอน":
                    invoicenumber = random_invoice_number_qr()
                    # check invoice number ซ้ำหรือไม่
                    while RegisterModel.objects.filter(invoice_number = invoicenumber):
                        invoicenumber = random_invoice_number_qr()

                elif getthis_paywithvoucher == "บัตรเครดิต":
                    invoicenumber = random_invoice_number_credit()
                    # check invoice number ซ้ำหรือไม่
                    while RegisterModel.objects.filter(invoice_number = invoicenumber):
                        invoicenumber = random_invoice_number_credit()



                print("CHANNEL ID", getthisregis.id)

                regismodel = RegisterModel.objects.get(id=getthisregis.id)
                # save invoice number
                regismodel.invoice_number = invoicenumber
                # save class
                regismodel.classroom = thisclass
                #
                regismodel.email = getemail
                regismodel.titlename_other = gettitlenameother
                regismodel.name = getname
                regismodel.lastname = getlastname
                regismodel.phone = getphone
                regismodel.jobs = getjob

                regismodel.haveaccout = gethaveaccout
                regismodel.oldaccout = getoldaccout
                regismodel.receipt = getreceipt

                #บุคคลธรรมดาindividual
                regismodel.indiname = getindiname
                regismodel.indilastname = getindilastname
                regismodel.inditaxid = getinditaxid

                regismodel.indiaddress = getindiaddress
                regismodel.indicity = getindicity
                regismodel.indistate = getindistate
                regismodel.indipostal = getindipostal
                regismodel.indicountry = getindicountry

                regismodel.indiaddress_send = getindiaddress_send
                regismodel.indicity_send = getindicity_send
                regismodel.indistate_send = getindistate_send
                regismodel.indipostal_send = getindipostal_send
                regismodel.indicountry_send = getindicountry_send

                #องค์กรorganization
                regismodel.orgname = getorgname

                regismodel.orgaddress1 = getorgaddress1
                regismodel.orgaddress2 = getorgaddress2
                regismodel.orgcity = getorgcity
                regismodel.orgstate = getorgstate
                regismodel.orgpostal = getorgpostal
                regismodel.orgcountry = getorgcountry

                regismodel.orgaddress1_send = getorgaddress1_send
                regismodel.orgaddress2_send = getorgaddress2_send
                regismodel.orgcity_send = getorgcity_send
                regismodel.orgstate_send = getorgstate_send
                regismodel.orgpostal_send = getorgpostal_send
                regismodel.orgcountry_send = getorgcountry_send

                regismodel.orgtaxid = getorgtaxid

                regismodel.taxwithholding = gettaxwithholding

                # regismodel.acctype = getacctype
                regismodel.imageevidence = getimageevidence
                # regismodel.imageevidence_data = getimageevidence_data

                # regismodel.paymenttype = getpaymenttype

                # regismodel.paywithvoucher = getpaywithvoucher
                regismodel.imagevoucherevidence = getimagevoucherevidence
                # regismodel.imagevoucherevidence_data = getimagevoucherevidence_data

                regismodel.acceptall = getacceptall
                
                regismodel.save()

                # messages.success(request, 'ลงทะเบียนสำเร็จ')
                # return redirect('home')
                # return redirect('signup', regisid=getthisregis.id)
                
                # get taxid
                if getthis_receipt == 'นามบุคคล':
                    taxid = getinditaxid
                elif getthis_receipt == 'นามองค์กร':
                    taxid = getorgtaxid

                # get product id
                thisclass = ClassroomModel.objects.get(id=classcode)
                productid = thisclass.product_id

                try:
                    data = {
                        'email':getemail,
                        'price':nowprice,
                        'getthis_acctype':getthis_acctype,
                        'regisid':getthisregis.id,
                        'taxid':taxid,
                        'invoicenumber':invoicenumber,
                        'productid':productid,
                        'gettaxwithholding':gettaxwithholding,
                        'vouchermargin':thisvoucher.margin,
                    }
                except:
                    data = {
                        'email':getemail,
                        'price':nowprice,
                        'getthis_acctype':getthis_acctype,
                        'regisid':getthisregis.id,
                        'taxid':taxid,
                        'invoicenumber':invoicenumber,
                        'productid':productid,
                        'gettaxwithholding':gettaxwithholding,
                    }
                    pass
                
                json_data = json.dumps(data)
                encoded_json_data = urlsafe_base64_encode(force_bytes(json_data))

                if getthis_paymenttype == "เงินโอน":
                    return redirect('checkouttransfer', data=encoded_json_data)
                elif getthis_paymenttype == "บัตรเครดิต":
                    return redirect('checkoutcredit', data=encoded_json_data)
                elif getthis_paywithvoucher == "เงินโอน":
                    return redirect('checkoutvouchertransfer', data=encoded_json_data)
                elif getthis_paywithvoucher == "บัตรเครดิต":
                    return redirect('checkoutvouchercredit', data=encoded_json_data)
            
            else:
                print(regisform.errors.as_data()) # here you print errors to terminal

        except:
            messages.error(request, 'เกิดข้อผิดพลาด')
            return redirect('registerform')
    
    context = {
        'regisform':regisform,
        'classcode':classcode,
        'thisclass':thisclass,
        'thisvoucher':thisvoucher,
    }
    return render(request, 'app_general/registerform.html', context)

def checkouttransfer(request, data):
    json_decoded_data = force_str(urlsafe_base64_decode(data))
    jsondata = json.loads(json_decoded_data)

    price = float(jsondata['price'])
    acctype = jsondata['getthis_acctype']
    email = jsondata['email']
    invoicenumber = jsondata['invoicenumber']
    productid = jsondata['productid']
    gettaxwithholding = jsondata['gettaxwithholding']

    # หักภาษีณที่จ่ายไหม
    withholding = 0
    if gettaxwithholding == 'WHT':
        withholding = price * 0.03
    elif gettaxwithholding == 'eWHT':
        withholding = price * 0.02
    
    vat = price * 0.07

    if acctype == 'สมาชิกสมาคม':
        discount = 300
        allprice = price - 300 + vat - withholding
    elif acctype == 'นิสิต/นักศึกษา':
        discount = 1000
        allprice = price - 1000 + vat - withholding
    elif acctype == 'บุคคลทั่วไป':
        discount = 0
        allprice = price + vat - withholding
    
    regisid = jsondata['regisid']
    print(allprice)

    #
    if request.method == 'POST':
        try:
            # generate api token
            # app_id = 'CMSK-FORM'
            # secret_key = '9kC0nGN2jLon3Uv91q5VKODYhHLR4nlQ'
            # url1 = "https://pgwuat.mycmsk.com/api/v1/token/create/" + app_id + "/" + secret_key
            # headers1 = {
            #     'accept': 'application/json',
            # }

            # r1 = requests.get(url1, headers=headers1)
            # print(r1.status_code)
            # print(r1.json())
            # print(r1.json()['token'])

            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJDTVNLLUZPUk0iLCJpYXQiOjE2NzYzNjcwMjEsImV4cCI6MTk5MTcyNzAyMX0.8o5m5zFYch2cKFCkbw0QJ3XLBgaJ-bkhjP17E-8wzVo'

            url = "https://pgwuat.mycmsk.com/api/v1/scb/payment/qr/create"
            # url = "https://pgw.mycmsk.com/api/v1/scb/payment/qr/create"
            headers = {
                'accept': 'application/json',
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
            bodydata = {
                "amount": str(allprice),
                "ref1": str(invoicenumber),
                "ref2": str(productid), #ใช้ REF2 แล้วได้ ?
                "email": str(email),
            }


            r = requests.post(url, headers=headers, json=bodydata)
            print(r.status_code)
            print(r.json())
            # print(r.json()['qrUrl'])

            # getdata = r.json()
            # json_data = json.dumps(getdata)
            # encoded_json_data = urlsafe_base64_encode(force_bytes(json_data))

            getdata = {
                'qrUrl':r.json()['qrUrl'],
                'amount':str(allprice),
                'request_id':r.json()['request_id'],
            }
            json_data = json.dumps(getdata)
            encoded_json_data = urlsafe_base64_encode(force_bytes(json_data))

            return redirect('qrtransfer', data=encoded_json_data)
        except:
            messages.error(request, 'ผิดพลาด')

    context = {
        'price':price,
        'vat':vat,
        'allprice':allprice,
        'regisid':regisid,
        'discount':discount,
        'withholding':withholding,
        'gettaxwithholding':gettaxwithholding,
        'invoicenumber':invoicenumber,
        'data':data,
    }
    return render(request, 'app_general/checkouttransfer.html', context)

def qrtransfer(request, data):
    json_decoded_data = force_str(urlsafe_base64_decode(data))
    jsondata = json.loads(json_decoded_data)
    print(jsondata)

    qrurl = jsondata['qrUrl']
    amount = jsondata['amount']
    request_id = jsondata['request_id']
    # print(qrurl)

    context = {
        'qrurl':qrurl,
        'amount':amount,
        'request_id':request_id
    }
    return render(request, 'app_general/qrtransfer.html', context)

def checkoutcredit(request, data):
    json_decoded_data = force_str(urlsafe_base64_decode(data))
    jsondata = json.loads(json_decoded_data)

    price = float(jsondata['price'])
    acctype = jsondata['getthis_acctype']
    email = jsondata['email']
    invoicenumber = jsondata['invoicenumber']
    productid = jsondata['productid']
    gettaxwithholding = jsondata['gettaxwithholding']

    # หักภาษีณที่จ่ายไหม
    withholding = 0
    if gettaxwithholding == 'WHT':
        withholding = price * 0.03
    elif gettaxwithholding == 'eWHT':
        withholding = price * 0.02

    vat = price * 0.07
    credit_fee = price * 0.03

    if acctype == 'สมาชิกสมาคม':
        discount = 300
        allprice = price - 300 + vat - withholding + credit_fee
    elif acctype == 'นิสิต/นักศึกษา':
        discount = 1000
        allprice = price - 1000 + vat - withholding + credit_fee
    elif acctype == 'บุคคลทั่วไป':
        discount = 0
        allprice = price + vat - withholding + credit_fee

    regisid = jsondata['regisid']

    #
    if request.method == 'POST':
        try:
            # generate api token
            # app_id = 'CMSK-FORM'
            # secret_key = '9kC0nGN2jLon3Uv91q5VKODYhHLR4nlQ'
            # url1 = "https://pgwuat.mycmsk.com/api/v1/token/create/" + app_id + "/" + secret_key
            # headers1 = {
            #     'accept': 'application/json',
            # }

            # r1 = requests.get(url1, headers=headers1)
            # print(r1.status_code)
            # print(r1.json())
            # print(r1.json()['token'])

            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJDTVNLLUZPUk0iLCJpYXQiOjE2NzYzNjcwMjEsImV4cCI6MTk5MTcyNzAyMX0.8o5m5zFYch2cKFCkbw0QJ3XLBgaJ-bkhjP17E-8wzVo'

            url = "https://pgwuat.mycmsk.com/api/v1/2c2p/payment/token/create"
            # url = "https://pgw.mycmsk.com/api/v1/2c2p/payment/token/create"
            headers = {
                'accept': 'application/json',
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
            bodydata = {
                "amount": allprice,
                "invoiceNo": invoicenumber,
                "description": productid,
                "email": email,
                "frontendReturnUrl": request.build_absolute_uri('/checkoutredirect'),
            }

            r = requests.post(url, headers=headers, json=bodydata)
            print(r.status_code)
            print(r.json())
            print(r.json()['webPaymentUrl'])
            url2c2p = str(r.json()['webPaymentUrl'])

            return HttpResponseRedirect(url2c2p)
        except:
            messages.error(request, 'ผิดพลาด')

    context = {
        'price':price,
        'vat':vat,
        'allprice':allprice,
        'regisid':regisid,
        'discount':discount,
        'withholding':withholding,
        'gettaxwithholding':gettaxwithholding,
        'invoicenumber':invoicenumber,
        'credit_fee':credit_fee,
        'data':data,
    }
    return render(request, 'app_general/checkoutcredit.html', context)

def checkoutvouchertransfer(request, data):
    json_decoded_data = force_str(urlsafe_base64_decode(data))
    jsondata = json.loads(json_decoded_data)

    price = float(jsondata['price'])
    vouchermargin = float(jsondata['vouchermargin'])
    acctype = jsondata['getthis_acctype']
    email = jsondata['email']
    invoicenumber = jsondata['invoicenumber']
    productid = jsondata['productid']
    gettaxwithholding = jsondata['gettaxwithholding']
    vat = price * 0.07
    # allprice = price + vat
    allprice = vouchermargin

    regisid = jsondata['regisid']

    #
    if request.method == 'POST':
        try:
            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJDTVNLLUZPUk0iLCJpYXQiOjE2NzYzNjcwMjEsImV4cCI6MTk5MTcyNzAyMX0.8o5m5zFYch2cKFCkbw0QJ3XLBgaJ-bkhjP17E-8wzVo'

            url = "https://pgwuat.mycmsk.com/api/v1/scb/payment/qr/create"
            # url = "https://pgw.mycmsk.com/api/v1/scb/payment/qr/create"
            headers = {
                'accept': 'application/json',
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
            bodydata = {
                "amount": str(allprice),
                "ref1": str(invoicenumber),
                "ref2": str(productid), #ใช้ REF2 แล้วได้ ?
                "email": str(email),
            }


            r = requests.post(url, headers=headers, json=bodydata)
            print(r.status_code)
            print(r.json())
            # print(r.json()['qrUrl'])

            # getdata = r.json()
            # json_data = json.dumps(getdata)
            # encoded_json_data = urlsafe_base64_encode(force_bytes(json_data))

            getdata = {
                'qrUrl':r.json()['qrUrl'],
                'amount':str(allprice),
                'request_id':r.json()['request_id'],
            }
            json_data = json.dumps(getdata)
            encoded_json_data = urlsafe_base64_encode(force_bytes(json_data))

            return redirect('qrtransfer', data=encoded_json_data)
        except:
            messages.error(request, 'ผิดพลาด')

    context = {
        'price':price,
        'vat':vat,
        'allprice':allprice,
        'regisid':regisid,
        'vouchermargin':vouchermargin,
        'data':data,
    }
    return render(request, 'app_general/checkoutvouchertransfer.html', context)

def checkoutvouchercredit(request, data):
    json_decoded_data = force_str(urlsafe_base64_decode(data))
    jsondata = json.loads(json_decoded_data)

    price = float(jsondata['price'])
    vouchermargin = float(jsondata['vouchermargin'])
    acctype = jsondata['getthis_acctype']
    email = jsondata['email']
    invoicenumber = jsondata['invoicenumber']
    productid = jsondata['productid']
    gettaxwithholding = jsondata['gettaxwithholding']
    vat = price * 0.07
    allprice = vouchermargin

    regisid = jsondata['regisid']

    #
    if request.method == 'POST':
        try:
            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJDTVNLLUZPUk0iLCJpYXQiOjE2NzYzNjcwMjEsImV4cCI6MTk5MTcyNzAyMX0.8o5m5zFYch2cKFCkbw0QJ3XLBgaJ-bkhjP17E-8wzVo'

            url = "https://pgwuat.mycmsk.com/api/v1/2c2p/payment/token/create"
            # url = "https://pgw.mycmsk.com/api/v1/2c2p/payment/token/create"
            headers = {
                'accept': 'application/json',
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            }
            bodydata = {
                "amount": allprice,
                "invoiceNo": invoicenumber,
                "description": productid,
                "email": email,
                "frontendReturnUrl": request.build_absolute_uri('/checkoutredirect'),
            }

            r = requests.post(url, headers=headers, json=bodydata)
            print(r.status_code)
            print(r.json())
            print(r.json()['webPaymentUrl'])
            url2c2p = str(r.json()['webPaymentUrl'])

            return HttpResponseRedirect(url2c2p)
        except:
            messages.error(request, 'ผิดพลาด')

    context = {
        'price':price,
        'vat':vat,
        'allprice':allprice,
        'regisid':regisid,
        'vouchermargin':vouchermargin,
        'data':data,
    }
    return render(request, 'app_general/checkoutvouchercredit.html', context)

@csrf_exempt
def checkoutredirect(request):
    return render(request, 'app_general/checkoutredirect.html')

def signup(request, regisid):
    
    if request.method == 'POST':
        signupname = request.POST['signupname']
        signuppass = request.POST['signuppass']

        if User.objects.filter(username=signupname):
            messages.error(request, 'ชื่อผู้ใช้นี้ถูกใช้แล้ว')
            return redirect('signup')

        # ต้องใช้ create_user ถึงจะบันทึกลงdatabaseได้ถูกต้อง
        # myuser = User.objects.create_user(username=input_username, email=input_email, password=input_password)
        # myuser.first_name = input_first_name
        # myuser.last_name = input_last_name

        # myuser.is_active = False

        # create user
        try:
            myuser = User.objects.create_user(username=signupname, password=signuppass)
            myuser.is_active = True

            myuser.save()

            # add user group
            group = Group.objects.get(name='customer_crud')
            myuser.groups.add(group)

            messages.success(request, 'สร้างบัญชีสำเร็จ')
            messages.add_message(request, SIGNUPSUCCESS, 'โปรดตรวจสอบอีเมลของท่าน')
            # return redirect('home')

            # ส่งอีเมล
            # gmailที่ใช้ ต้องเปิด2faของมันเอง แล้วไปที่apppasswordเอาpasswordที่generateมาใส่

            current_site = get_current_site(request)
            email_subject = 'ยินดีต้อนรับสู่"CRUD"'
            
            message_greeting = render_to_string('app_general/email/email_greeting.html', {
                'name':myuser.username,
            })

            email = EmailMessage(
                email_subject,
                message_greeting,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

        except:
            messages.error(request, 'ผิดพลาด')

    context = {
        'regisid': regisid,
    }
    return render(request, 'app_general/signup.html', context)

def signin(request):

    if request.method == 'POST':
        try:
            getusername = request.POST['signinusername']
            getpassword = request.POST['signinpassword']

            signinuser = authenticate(username=getusername, password=getpassword)

            if signinuser is not None:
                login(request, signinuser)
                messages.success(request, 'ลงชื่อเข้าใช้สำเร็จ')
                return redirect('home')

            else:
                messages.error(request, 'ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง!')
                return redirect('signin')
        except:
            pass

    return render(request, 'app_general/signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'คุณได้ลงชื่อออกแล้ว')
    return redirect('home')