from django.db import models

class UserLogin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=8)
    utype = models.CharField(max_length=50)

class UserRegistration(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    pincode = models.IntegerField()
    email = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)
    profile_photo = models.FileField(upload_to='DOCUMENT/')


class AddDealers(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    pincode = models.IntegerField()
    email = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)

class MarketPrice(models.Model):
    cotton_level = models.CharField(max_length=50,null=True,blank=True)
    uom = models.CharField(max_length=50,null=True,blank=True)
    price = models.CharField(max_length=50,null=True,blank=True)
    #created_date = models.DateField(auto_now_add=True,null=True,blank=True)

class CottonRequest(models.Model):
    user_id = models.CharField(max_length=50,null=True)
    cotton_type = models.CharField(max_length=50,null=True)
    uom = models.CharField(max_length=50,null=True)
    qty = models.IntegerField(null=True)
    request_date=models.DateField(null=True)
    request_time=models.CharField(max_length=20,null=True)
    request_status=models.CharField(max_length=40,null=True)
    #date=models.CharField(max_length=500,null=True)
    date = models.DateField(null=True, blank=True)
    cotton_photo = models.FileField(upload_to='DOCUMENT/',null=True)
    received_status = models.CharField(max_length=40, null=True)
    payment_status = models.CharField(max_length=40, null=True)
    total_amount = models.FloatField(null=True, blank=True)
    #is_notified = models.BooleanField(default=False)



class FarmerPayment(models.Model):
    user_id = models.CharField(max_length=50)
    cotton_type = models.CharField(max_length=50)
    total_qty = models.CharField(max_length=50)
    unit_price = models.IntegerField()
    total=models.IntegerField()
    payment_status=models.CharField(max_length=20)
    payment_date=models.DateField()


class CottonSeparation(models.Model):
    total_qty = models.IntegerField(null=True)
    separation_type = models.CharField(max_length=50,null=True)
    uom = models.CharField(max_length=50,null=True)
    date=models.DateField(null=True)


class OtpCode(models.Model):
    otp = models.IntegerField(null=True)
    status = models.CharField(max_length=50,null=True)



