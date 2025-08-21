from django.shortcuts import render,redirect
from django.http import JsonResponse
from cotton_app.models import UserLogin,OtpCode,AddDealers,UserRegistration,MarketPrice,CottonRequest,FarmerPayment,CottonSeparation
import os
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
#import datetime
#from datetime import date

from datetime import datetime
from django.conf import settings


from datetime import datetime, date
from .models import CottonRequest
from django.db.models import Avg,Max,Min,Sum,Count
from django.urls import reverse
import smtplib
import random

def get_new_cotton_count(request):
    from cotton_app.models import CottonRequest
    if request.method == 'GET':
        count = CottonRequest.objects.filter(request_status='pending').count()
        return JsonResponse({'count': count})
    
def index(request):
    return render(request,'index.html')

def admin_home(request):
    new_requests = CottonRequest.objects.filter(request_status='pending').count()
    return render(request, 'admin_home.html', {'cotton_count': new_requests})


def user_home(request):
    return render(request,'user_home.html')



def login(request):
    if request.method=="POST":
        username=request.POST.get('t1')
        password=request.POST.get('t2')
        request.session['username']=username
        count=UserLogin.objects.filter(username=username).count()
        if count>=1:
            udata=UserLogin.objects.get(username=username)
            pwd=udata.password
            utype=udata.utype
            print(password,pwd)
            if password == pwd:
                if utype=="admin":
                    return redirect('admin_home')
                if utype=="user":
                    return redirect('user_home')
                if utype=='supplier':
                    return redirect('supplier_home')

            else:
                return render(request,'login.html',{'msg':'Invalid Password'})
        else:
            return render(request,'login.html',{'msg':'invalid username'})


    return render(request,'login.html')



def reg(request):
    if request.method=="POST" and request.FILES['file']:
        fname=request.POST.get('t1')
        lname = request.POST.get('t2')
        gender = request.POST.get('t3')
        address = request.POST.get('t4')
        pincode = request.POST.get('t5')
        email = request.POST.get('t6')
        mobile_no = request.POST.get('t7')
        profile_photo=request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(profile_photo.name, profile_photo)
        fileurl = fs.url(filename)
        password = request.POST.get('t8')
        count=UserRegistration.objects.filter(email=email).count()
        if count>=1:
            return render(request,'reg.html',{'msg':'User is already existed'})
        else:
            UserRegistration.objects.create(fname=fname,lname=lname,gender=gender,address=address,pincode=pincode,email=email,mobile_no=mobile_no,profile_photo=profile_photo)
            UserLogin.objects.create(username=email,password=password,utype='user')
            return render(request, 'reg.html', {'popup': True})

    return render(request,'reg.html')


def add_dealers(request):
    if request.method=="POST":
        fname=request.POST.get('t1')
        lname = request.POST.get('t2')
        address = request.POST.get('t4')
        pincode = request.POST.get('t5')
        email = request.POST.get('t6')
        mobile_no = request.POST.get('t7')
        AddDealers.objects.create(fname=fname,lname=lname,address=address,pincode=pincode,email=email,mobile_no=mobile_no)
        UserLogin.objects.create(username=email,password=mobile_no,utype='dealer')
        return render(request, 'add_dealers.html',{'msg':'Added Successfully'})

    return render(request,'add_dealers.html')

def cotton_request_noti(request):
    # Only get pending requests
    pending_requests = CottonRequest.objects.filter(request_status__iexact='Pending')
    return render(request, 'cotton_request_noti.html', {'userdict': pending_requests})

#def cotton_request_notiSS(request):
 #   userdict=CottonRequest.objects.all()
  #  return render(request,'cotton_request_noti.html',{'userdict':userdict})

def reg_view(request):
    userdict=UserRegistration.objects.all()
    return render(request,'reg_view.html',{'userdict':userdict})

def dealers_view(request):
    userdict=AddDealers.objects.all()
    return render(request,'dealers_view.html',{'userdict':userdict})


def market_price(request):
    if request.method=="POST":
        cotton_level=request.POST.get('t1')
        uom=request.POST.get('t2')
        price=request.POST.get('t3')
        MarketPrice.objects.create(cotton_level=cotton_level,uom=uom,price=price)
        return render(request,'market_price.html',{'msg':'Added Successfully'})
    return render(request,'market_price.html')


def cotton_separation(request):
    n = datetime.now()  # ✅ correct

    #n=datetime.datetime.now()
    ndate=n.strftime("%Y-%m-%d")
    if request.method=="POST":
        separation_type=request.POST.get('t1')
        uom = request.POST.get('t2')
        total_qty = request.POST.get('t4')
        date = request.POST.get('date')

        CottonSeparation.objects.create(separation_type=separation_type,total_qty=total_qty,uom=uom,date=date)
        return render(request, 'cotton_separation.html',{'msg':'Added Successfully','d':ndate})
    return render(request,'cotton_separation.html',{'d':ndate})



'''def cotton_separation_view(request):
    userdict = CottonSeparation.objects.all()
    return render(request,'cotton_separation_view.html',{'userdict':userdict})'''
def cotton_separation_view(request):
    userdict = CottonSeparation.objects.all()

    # Calculate total quantity for each separation type
    cleaned = CottonSeparation.objects.filter(separation_type="cleaned_cotton").aggregate(Sum('total_qty'))['total_qty__sum'] or 0
    pressed = CottonSeparation.objects.filter(separation_type="pressed_cotton").aggregate(Sum('total_qty'))['total_qty__sum'] or 0
    wastage = CottonSeparation.objects.filter(separation_type="wastage_cotton").aggregate(Sum('total_qty'))['total_qty__sum'] or 0
    uncleaned = CottonSeparation.objects.filter(separation_type="uncleaned_cotton").aggregate(Sum('total_qty'))['total_qty__sum'] or 0

    context = {
        'userdict': userdict,
        'cleaned': cleaned,
        'pressed': pressed,
        'wastage': wastage,
        'uncleaned': uncleaned,
    }
    return render(request, 'cotton_separation_view.html', context)


def cotton_request(request):
    user_id = request.session['username']
    n = datetime.now()
    request_date = n.strftime("%Y-%m-%d")
    request_time = n.strftime("%X")
    prices = MarketPrice.objects.all()

    if request.method == "POST" and request.FILES.get('file'):
        cotton_type = request.POST.get('t1')
        uom = request.POST.get('t2')
        qty = float(request.POST.get('t3'))
        cotton_photo = request.FILES['file']

        # ✅ Handle multiple matching records safely
        price_qs = MarketPrice.objects.filter(cotton_level=cotton_type, uom=uom)
        if price_qs.exists():
            price_obj = price_qs.latest('id')  # or .first()
            unit_price = float(price_obj.price)
            total_amount = unit_price * qty
        else:
            total_amount = None

        fs = FileSystemStorage()
        filename = fs.save(cotton_photo.name, cotton_photo)
        fileurl = fs.url(filename)

        CottonRequest.objects.create(
            user_id=user_id,
            cotton_type=cotton_type,
            uom=uom,
            qty=qty,
            request_date=request_date,
            request_time=request_time,
            request_status='pending',
            date=date.today(),
            cotton_photo=cotton_photo,
            total_amount=total_amount
        )

        return render(request, 'cotton_request.html', {'popup': True})

    return render(request, 'cotton_request.html', {'prices': prices})




def cotton_request_view(request):
    username=request.session['username']
    userdict=CottonRequest.objects.filter(user_id=username).values()
    return render(request,'cotton_request_view.html',{'userdict':userdict})

def cotton_sep_del(request,pk):
    udata=CottonSeparation.objects.get(id=pk)
    udata.delete()
    return redirect('cotton_separation_view')

def cotton_sep_edit(request,pk):
    udata=CottonSeparation.objects.filter(id=pk).values()
    if request.method=="POST":
        separation_type=request.POST.get('t1')
        uom = request.POST.get('t2')
        total_qty = request.POST.get('t4')
        date = request.POST.get('date')
        CottonSeparation.objects.filter(id=pk).update(separation_type=separation_type,total_qty=total_qty,uom=uom,date=date)
        return redirect('cotton_separation_view')
    return render(request,'cotton_sep_edit.html',{'udata':udata})

def dealer_del(request,pk):
    udata=AddDealers.objects.get(id=pk)
    udata.delete()
    return redirect('dealers_view')

def dealer_edit(request,pk):
    udata=AddDealers.objects.filter(id=pk).values()
    if request.method=="POST":
        fname=request.POST.get('t1')
        lname = request.POST.get('t2')
        address = request.POST.get('t4')
        pincode = request.POST.get('t5')
        email = request.POST.get('t6')
        mobile_no = request.POST.get('t7')
        AddDealers.objects.filter(id=pk).update(fname=fname,lname=lname,address=address,pincode=pincode,email=email,mobile_no=mobile_no)
        return redirect('dealers_view')
    return render(request,'dealer_edit.html',{'udata':udata})

def reg_del(request,pk):
    udata=UserRegistration.objects.get(id=pk)
    udata.delete()
    return redirect('reg_view')

def approve_request(request, pk):
    if request.method == "POST":
        status = request.POST.get('t1')
        date = request.POST.get('t2')

        # Update DB
        CottonRequest.objects.filter(id=pk).update(request_status=status, date=date)

        # Get user email and cotton type
        req = CottonRequest.objects.get(id=pk)
        user_email = req.user_id
        cotton_type = req.cotton_type

        # Email content
        if status == "Accepted":
            subject = "Cotton Request Approved"
            message = f"Your cotton request for '{cotton_type}' has been approved. Please bring the cotton before {date}."
        else:
            subject = "Cotton Request Rejected"
            message = f"Your cotton request for '{cotton_type}' has been rejected. Please contact us for further details."

        # Send email
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )

        return redirect('cotton_request_view_a')

    return render(request, 'approve_request.html', {'popup': True})


def update_received_status(request,pk):
    if request.method=="POST":
        status=request.POST.get('t1')
        CottonRequest.objects.filter(id=pk).update(received_status=status)
        return redirect('cotton_request_view_a')
    return render(request,'update_received_status.html')


def cotton_request_view_a(request):
    userdict=CottonRequest.objects.all()
    return render(request,'cotton_request_view_a.html',{'userdict':userdict})

def received_cottons(request):
    userdict = CottonRequest.objects.filter(received_status='Received').values()
    total = CottonRequest.objects.filter(received_status='Received').aggregate(total=Sum("qty"))['total']
    return render(request,'received_cottons.html',{'userdict':userdict,'total':total})


def farmers_payment(request):
    udata=CottonRequest.objects.filter(received_status='Received').values()
    return render(request,'farmers_payment.html',{'udata':udata})

def farmer_payment_next(request,pk):
    udata=CottonRequest.objects.get(id=pk)
    qty=int(udata.qty)
    uid=udata.user_id
    cotton_type=udata.cotton_type
    #n=datetime.datetime.now()
    n = datetime.now()
    payment_date=n.strftime("%Y-%m-%d")
    if request.method=="POST":
        price=request.POST.get('t2')
        total = request.POST.get('t3')
        CottonRequest.objects.filter(id=pk).update(payment_status='Paid')
        FarmerPayment.objects.create(user_id=uid,cotton_type=cotton_type,total_qty=qty,unit_price=price,total=total,payment_status='Paid',payment_date=payment_date)
        return render(request,'online_payment.html',{'amount':total})
    return render(request,'farmers_payment_next.html',{'qty':qty})

def payment_msg(request):
    return render(request,'payment_msg.html')


def market_price_view(request):
    userdict=MarketPrice.objects.all()
    return render(request,'market_price_view.html',{'userdict':userdict})

def market_price_view_u(request):
    userdict=MarketPrice.objects.all()
    return render(request,'market_price_view_u.html',{'userdict':userdict})

def payment_view_farmer(request):
    username=request.session['username']
    udata=FarmerPayment.objects.filter(user_id=username).values()
    return render(request,'payment_view_farmer.html',{'udata':udata})

def payment_view_admin(request):
    udata=FarmerPayment.objects.all()
    return render(request,'payment_view_admin.html',{'udata':udata})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


def forgotpass(request):
    if request.method=="POST":
        username=request.POST.get('t1')
        request.session['username']=username
        ucheck=UserLogin.objects.filter(username=username).count()
        if ucheck>=1:
            otp = random.randint(1111, 9999)
            OtpCode.objects.create(otp=otp, status='active')
            content = "Your OTP IS-" + str(otp)
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('akshatainaik90@gmail.com','ceojgvrjhjomlbhd')
            mail.sendmail('akshatainaik90@gmail.com',username,content)
            base_url = reverse('otp')
            return redirect(base_url)
        else:
            return render(request,'forgotpass.html',{'msg':'Invalid Username'})
    return render(request,'forgotpass.html')

def otp(request):
    if request.method=="POST":
        otp=request.POST.get('t1')
        ucheck=OtpCode.objects.filter(otp=otp).count()
        if ucheck>=1:
            base_url = reverse('resetpass')
            return redirect(base_url)
        else:
            return render(request,'otp.html',{'msg':'Invalid OTP'})
    return render(request,'otp.html')


def resetpass(request):
    username=request.session['username']
    if request.method=="POST":
        newpass=request.POST.get('t1')
        confirmpass=request.POST.get('t2')
        if newpass==confirmpass:
            UserLogin.objects.filter(username=username).update(password=newpass)
            base_url=reverse('login')
            return redirect(base_url)
        else:
            return render(request,'resetpass.html',{'msg':'New password and confirm password must be same'})
    return render(request,'resetpass.html')


def cotton_req_del(request,pk):
    udata=CottonRequest.objects.get(id=pk)
    udata.delete()
    return redirect('cotton_request_view')

def market_del(request,pk):
    udata=MarketPrice.objects.get(id=pk)
    udata.delete()
    return redirect('market_price_view')


def market_edit(request,pk):
    udata=MarketPrice.objects.filter(id=pk).values()
    if request.method == "POST":
        cotton_level = request.POST.get('t1')
        uom = request.POST.get('t2')
        price = request.POST.get('t3')
        date = request.POST.get('t4')
        MarketPrice.objects.filter(id=pk).update(cotton_level=cotton_level,uom=uom,price=price)
        return redirect('market_price_view')
    return render(request,'market_edit.html',{'udata':udata})

from django.db.models import Sum
from datetime import datetime

def purchase_cotton(request):
    if request.method == "POST":
        month = request.POST.get('month')
        search = request.POST.get('search')  # specific date

        data = CottonRequest.objects.none()
        total_kg = total_quintal = total_all_kg = 0

        # Month-wise filter
        if month:
            try:
                # Convert month string (e.g., "2025-06") to year and month
                selected_month = datetime.strptime(month, "%Y-%m")
                data = CottonRequest.objects.filter(
                    request_date__year=selected_month.year,
                    request_date__month=selected_month.month,
                    received_status__iexact="Received"
                )
            except ValueError:
                pass  # handle invalid month format if necessary

        # Date-wise filter
        elif search:
            try:
                data = CottonRequest.objects.filter(
                    request_date=search,
                    received_status__iexact="Received"
                )
            except ValueError:
                pass

        total_kg = data.filter(uom="Kg").aggregate(total=Sum('qty'))['total'] or 0
        total_quintal = data.filter(uom="Quintal").aggregate(total=Sum('qty'))['total'] or 0
        total_all_kg = total_kg + (total_quintal * 100)

        return render(request, 'purchase_cotton_report.html', {
            'data': data,
            'total_kg': total_kg,
            'total_quintal': total_quintal,
            'total_all_kg': total_all_kg,
            'search_date': search,
            'search_month': month,
        })

    return render(request, 'purchase_cotton.html')

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
import os
from io import BytesIO

def download_cotton_report(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    search = request.GET.get('search')

    data = CottonRequest.objects.none()

    if year:
        data = CottonRequest.objects.filter(request_date__year=year, received_status__iexact="Received")
    elif month:
        try:
            selected_month = datetime.strptime(month, "%Y-%m")
            data = CottonRequest.objects.filter(
                request_date__year=selected_month.year,
                request_date__month=selected_month.month,
                received_status__iexact="Received"
            )
        except:
            pass
    elif search:
        data = CottonRequest.objects.filter(request_date=search, received_status__iexact="Received")

    total_kg = data.filter(uom="Kg").aggregate(total=Sum('qty'))['total'] or 0
    total_quintal = data.filter(uom="Quintal").aggregate(total=Sum('qty'))['total'] or 0
    total_all_kg = total_kg + (total_quintal * 100)
    logo_path = os.path.abspath("cotton_app/static/assets/img/logo.png")
    logo_path = f"file:///{logo_path.replace(os.sep, '/')}"  # This ensures Windows compatibility

    context = {
        'data': data,
        'total_kg': total_kg,
        'total_quintal': total_quintal,
        'total_all_kg': total_all_kg,
        'logo_path': logo_path,
    }

    template_path = 'pdf_cotton_report.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="cotton_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response


def view_farmer(request,email):
    udata=UserRegistration.objects.filter(email=email).values()
    return render(request,'view_farmer.html',{'udata':udata})

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from cotton_app.models import UserLogin

def changepass(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    if request.method == "POST":
        old = request.POST.get('old')
        newpass = request.POST.get('t1')
        confirmpass = request.POST.get('t2')

        try:
            user = UserLogin.objects.get(username=username, utype='admin')
        except UserLogin.DoesNotExist:
            messages.error(request, "Admin user not found.")
            return redirect('login')

        if user.password != old:
            messages.error(request, "Invalid old password.")
        elif newpass != confirmpass:
            messages.error(request, "New password and confirm password must match.")
        else:
            user.password = newpass
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect('login')  # Change this if your admin login URL name is different

    return render(request, 'changepass.html')

def purchase_cotton1(request):
    if request.method == "POST":
        year = request.POST.get('year')
        month = request.POST.get('month')
        search = request.POST.get('search')  # specific date

        data = CottonRequest.objects.none()
        total_kg = total_quintal = total_all_kg = 0

        # Year filter
        if year:
            data = CottonRequest.objects.filter(
                request_date__year=year,
                received_status__iexact="Received"
            )

        # Month filter
        elif month:
            try:
                selected_month = datetime.strptime(month, "%Y-%m")
                data = CottonRequest.objects.filter(
                    request_date__year=selected_month.year,
                    request_date__month=selected_month.month,
                    received_status__iexact="Received"
                )
            except ValueError:
                pass

        # Date filter
        elif search:
            try:
                data = CottonRequest.objects.filter(
                    request_date=search,
                    received_status__iexact="Received"
                )
            except ValueError:
                pass

        total_kg = data.filter(uom="Kg").aggregate(total=Sum('qty'))['total'] or 0
        total_quintal = data.filter(uom="Quintal").aggregate(total=Sum('qty'))['total'] or 0
        total_all_kg = total_kg + (total_quintal * 100)

        return render(request, 'purchase_cotton1.html', {
            'data': data,
            'total_kg': total_kg,
            'total_quintal': total_quintal,
            'total_all_kg': total_all_kg,
            'search_date': search,
            'search_month': month,
            'search_year': year,
        })

    return render(request, 'purchase_cotton1.html')

'''def changepass_user(request):
    username = request.session.get('username')
    print("🧠 Session username:", username)

    if not username:
        return redirect('login')  # redirect to login if session expired

    if request.method == "POST":
        old = request.POST.get('old', '').strip()
        newpass = request.POST.get('t1', '').strip()
        confirmpass = request.POST.get('t2', '').strip()

        try:
            user = UserLogin.objects.get(username=username)
            print("✅ Found user:", user.username)
            print("🔐 DB password:", user.password)
            print("🔑 Entered old password:", old)
        except UserLogin.DoesNotExist:
            return render(request, 'changepass_user.html', {'msg': 'User not found'})

        if user.password == old:
            if newpass == confirmpass:
                user.password = newpass
                user.save()
                return redirect('login')
            else:
                return render(request, 'changepass_user.html', {'msg': 'New and Confirm Passwords do not match'})
        else:
            return render(request, 'changepass_user.html', {'msg': 'Invalid Old Password'})

    return render(request, 'changepass_user.html')'''

def changepass_user(request):
    username = request.session.get('username')

    if not username:
        return redirect('login')

    if request.method == "POST":
        old = request.POST.get('old', '').strip()
        newpass = request.POST.get('t1', '').strip()
        confirmpass = request.POST.get('t2', '').strip()

        try:
            user = UserLogin.objects.get(username=username)
        except UserLogin.DoesNotExist:
            return render(request, 'changepass_user.html', {'msg': 'User not found'})

        if user.password == old:
            if newpass == confirmpass:
                user.password = newpass
                user.save()
                messages.success(request, 'Password changed successfully! Please login again.')
                return redirect('login')
            else:
                messages.error(request, 'New and Confirm Passwords do not match')
        else:
            messages.error(request, 'Invalid Old Password')

    return render(request, 'changepass_user.html')

# views.py or cotton_app/utils.py

from django.core.mail import send_mail
from django.conf import settings

