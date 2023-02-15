from django.db import models

import datetime

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# Create your models here.

class CourseModel(models.Model):
    code = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    order_number = models.BigIntegerField(blank=True, null=True)
    # image = models.ImageField(blank=True, null=True, upload_to='imagecourse/')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.code)

CLASS_TYPE = [
    ('อบรมและทบทวน','อบรมและทบทวน'),
    ('อบรมเท่านั้น','อบรมเท่านั้น'),
    ('ทบทวนเท่านั้น','ทบทวนเท่านั้น'),
]
class ClassroomModel(models.Model):
    product_id = models.CharField(max_length=200, blank=True, null=True)
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, blank=True, null=True)
    class_type = models.CharField(choices=CLASS_TYPE, max_length=200, blank=True, null=True)
    
    generation = models.CharField(max_length=200, blank=True, null=True)

    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    earlybird_date_start = models.DateField(blank=True, null=True)
    earlybird_date_end = models.DateField(blank=True, null=True)
    price_earlybird = models.BigIntegerField(blank=True, null=True)

    promotion_date_start = models.DateField(blank=True, null=True)
    promotion_date_end = models.DateField(blank=True, null=True)
    price_promotion = models.BigIntegerField(blank=True, null=True)

    fullprice_date_start = models.DateField(blank=True, null=True)
    fullprice_date_end = models.DateField(blank=True, null=True)
    price_fullprice = models.BigIntegerField(blank=True, null=True)

    # price_full = models.BigIntegerField(blank=True, null=True)

    is_active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return str(self.product_id)

    @property
    def get_now_price(self):

        if self.course is not None:

            todaydate = datetime.date.today()

            earlybirddatestart = self.earlybird_date_start
            earlybirddateend = self.earlybird_date_end

            promotiondatestart = self.promotion_date_start
            promotiondateend = self.promotion_date_end

            fullpricedatestart = self.fullprice_date_start
            fullpricedateend = self.fullprice_date_end

            if todaydate >= earlybirddatestart and todaydate <= earlybirddateend:
                nowprice = self.price_earlybird
            elif todaydate >= promotiondatestart and todaydate <= promotiondateend:
                nowprice = self.price_promotion
            elif todaydate >= fullpricedatestart and todaydate <= fullpricedateend:
                nowprice = self.price_fullprice
            else:
                nowprice = self.price_fullprice

        return float(nowprice)

    @property
    def get_status_price(self):

        if self.course is not None:

            todaydate = datetime.date.today()

            earlybirddatestart = self.earlybird_date_start
            earlybirddateend = self.earlybird_date_end

            promotiondatestart = self.promotion_date_start
            promotiondateend = self.promotion_date_end

            fullpricedatestart = self.fullprice_date_start
            fullpricedateend = self.fullprice_date_end

            if todaydate >= earlybirddatestart and todaydate <= earlybirddateend:
                statusprice = 'earlybird'
            elif todaydate >= promotiondatestart and todaydate <= promotiondateend:
                statusprice = 'promotion'
            elif todaydate >= fullpricedatestart and todaydate <= fullpricedateend:
                statusprice = 'fullprice'
            else:
                statusprice = 'fullprice'
                
        return  statusprice

class VoucherModel(models.Model):
    classroom = models.OneToOneField(ClassroomModel, on_delete=models.CASCADE, blank=True, null=True)
    voucher_code = models.CharField(max_length=200, blank=True, null=True)
    margin = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.classroom)
class ChannelModel(models.Model):
    channel = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.channel)

TITLENAME = [
    ('นาย', 'นาย'),
    ('นาง', 'นาง'),
    ('นางสาว', 'นางสาว'),
    ('อื่นๆ', 'อื่นๆ'),
]
RECEIPTTYPE = [
    ('นามบุคคล', 'นามบุคคล'),
    ('นามองค์กร', 'นามองค์กร'),
]
ACCTYPE = [
    ('บุคคลทั่วไป', 'บุคคลทั่วไป'),
    ('สมาชิกสมาคม', 'สมาชิกสมาคม'),
    ('นิสิต/นักศึกษา', 'นิสิต/นักศึกษา'),
]
PAYMENTTYPE = [
    ("เงินโอน", "ชำระด้วย'เงินโอน'"),
    ("บัตรเครดิต", "ชำระด้วย'บัตรเครดิต'"),
    ("Voucher", "ใช้ Voucher"),
]
PAYMENVOUCHERTTYPE = [
    ("เงินโอน", "ชำระด้วย'เงินโอน'"),
    ("บัตรเครดิต", "ชำระด้วย'บัตรเครดิต'"),
    ("", ""),
]
class RegisterModel(models.Model):
    invoice_number = models.CharField(max_length=20, blank=True, null=True)
    classroom = models.ForeignKey(ClassroomModel, on_delete=models.CASCADE, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    titlename = models.CharField(choices=TITLENAME, max_length=200, blank=True, null=True)
    titlename_other = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    jobs = models.CharField(max_length=200, blank=True, null=True)
    
    channel = models.ManyToManyField(ChannelModel)

    haveaccout = models.BooleanField(default=None, blank=True, null=True)
    oldaccout = models.CharField(max_length=200, default=None, blank=True, null=True)
    
    # receipt = models.CharField(max_length=200, blank=True, null=True)
    receipt = models.CharField(choices=RECEIPTTYPE, max_length=200, blank=True, null=True)

    #บุคคลธรรมดาindividual
    indiname = models.CharField(max_length=200, blank=True, null=True)
    indilastname = models.CharField(max_length=200, blank=True, null=True)
    inditaxid = models.BigIntegerField(default=0, blank=True, null=True)

    indiaddress = models.CharField(max_length=200, blank=True, null=True)
    indicity = models.CharField(max_length=200, blank=True, null=True)
    indistate = models.CharField(max_length=200, blank=True, null=True)
    indipostal = models.CharField(max_length=200, blank=True, null=True)
    indicountry = models.CharField(max_length=200, blank=True, null=True)

    indiaddress_send = models.CharField(max_length=200, blank=True, null=True)
    indicity_send = models.CharField(max_length=200, blank=True, null=True)
    indistate_send = models.CharField(max_length=200, blank=True, null=True)
    indipostal_send = models.CharField(max_length=200, blank=True, null=True)
    indicountry_send = models.CharField(max_length=200, blank=True, null=True)
    
    #องค์กรorganization
    orgname = models.CharField(max_length=200, blank=True, null=True)

    orgaddress1 = models.CharField(max_length=200, blank=True, null=True)
    orgaddress2 = models.CharField(max_length=200, blank=True, null=True)
    orgcity = models.CharField(max_length=200, blank=True, null=True)
    orgstate = models.CharField(max_length=200, blank=True, null=True)
    orgpostal = models.CharField(max_length=200, blank=True, null=True)
    orgcountry = models.CharField(default='', max_length=200, blank=True, null=True)

    orgaddress1_send = models.CharField(max_length=200, blank=True, null=True)
    orgaddress2_send = models.CharField(max_length=200, blank=True, null=True)
    orgcity_send = models.CharField(max_length=200, blank=True, null=True)
    orgstate_send = models.CharField(max_length=200, blank=True, null=True)
    orgpostal_send = models.CharField(max_length=200, blank=True, null=True)
    orgcountry_send = models.CharField(default='', max_length=200, blank=True, null=True)

    orgtaxid = models.BigIntegerField(default=0, blank=True, null=True)
    #
    taxwithholding = models.CharField(max_length=200, blank=True, null=True)
    
    acctype = models.CharField(choices=ACCTYPE, max_length=200, blank=True, null=True)
    imageevidence = models.ImageField(blank=True, null=True, upload_to='imageevidence/')
    # imageevidence_data = models.BinaryField(blank=True, null=True)

    # paymenttype = models.CharField(max_length=200, blank=True, null=True)
    paymenttype = models.CharField(choices=PAYMENTTYPE, max_length=200, blank=True, null=True)
    
    paywithvoucher = models.CharField(choices=PAYMENVOUCHERTTYPE, max_length=200, blank=True, null=True)
    imagevoucherevidence = models.ImageField(blank=True, null=True, upload_to='imagevoucherevidence/')
    # imagevoucherevidence_data = models.BinaryField(blank=True, null=True)

    acceptall = models.BooleanField(default=None, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
@receiver(post_delete, sender=RegisterModel)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.imageevidence.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=RegisterModel)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = RegisterModel.objects.get(id=instance.id).imageevidence

        try:
            new_img = instance.imageevidence
        except:
            new_img = None

        if new_img != old_img:
            if old_img is not None:
                old_img.delete(save=False)
    except:
        pass

@receiver(post_delete, sender=RegisterModel)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.imagevoucherevidence.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=RegisterModel)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = RegisterModel.objects.get(id=instance.id).imagevoucherevidence

        try:
            new_img = instance.imagevoucherevidence
        except:
            new_img = None

        if new_img != old_img:
            if old_img is not None:
                old_img.delete(save=False)
    except:
        pass