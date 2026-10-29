from django.shortcuts import render,redirect
from.models import Equipment,Supplier,RentalRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth import login,authenticate,logout
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

def home(request):

    is_supplier = False

    if request.user.is_authenticated and hasattr(request.user, 'supplier'):
        is_supplier = True

    return render(request, 'home.html', {
        'is_supplier': is_supplier
    })

def equipment_list(request):
    equipments = Equipment.objects.all()

    location = request.GET.get('location')

    if location:
        equipments = equipments.filter(location__icontains=location)

    return render(request, 'equipment_list.html', {'equipments': equipments})

def equipment_detail(request, id):
    equipment = get_object_or_404(Equipment, id=id)

    rental_request = None
    is_supplier = False

    if request.user.is_authenticated:
        is_supplier = hasattr(request.user, 'supplier')

        rental_request = RentalRequest.objects.filter(
            equipment=equipment,
            buyer=request.user
        ).order_by('-id').first()

    return render(request, 'equipment_details.html', {
        'equipment': equipment,
        'rental_request': rental_request,
        'is_supplier': is_supplier,
    })

def equipment_by_type(request, type_name):
    equipments = Equipment.objects.filter(equipment_type=type_name)

    location = request.GET.get('location')

    if location:
        equipments = equipments.filter(location__icontains=location)
        
    return render(request, 'equipment_list.html', {
        'equipments': equipments,
        'selected_type': type_name
    })
def signup(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            role = form.cleaned_data['role']

            if role == 'supplier':

                Supplier.objects.create(
                    user=user,
                    company_name="New Supplier",
                    phone="",
                    address=""
                )

                login(request,user)
                return redirect('supplier_dashboard')

            else:

                login(request,user)
                return redirect('home')

    else:
        form = SignupForm()

    return render(request,'signup.html',{'form':form})

@login_required
def supplier_dashboard(request):

    if not hasattr(request.user,'supplier'):
        return redirect('home')

    supplier = request.user.supplier
    equipments = Equipment.objects.filter(supplier=supplier)

    return render(request,'supplier_dashboard.html',{
        'equipments':equipments,
        'supplier': supplier
    })

@login_required
def my_equipment(request):

    supplier = request.user.supplier
    equipments = Equipment.objects.filter(supplier=supplier)

    return render(request, 'my_equipment.html', {
        'equipments': equipments
    })

def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            if hasattr(user, 'supplier'):
                return redirect('supplier_dashboard')
            else:
                return redirect('home')

        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

@login_required
def add_equipment(request):

    supplier = request.user.supplier

    if request.method == "POST":

        name = request.POST['name']
        equipment_type = request.POST['equipment_type']
        description = request.POST['description']
        rent_per_day = request.POST['rent_per_day']
        location = request.POST['location']

        Equipment.objects.create(
            supplier=supplier,
            name=name,
            equipment_type=equipment_type,
            description=description,
            rent_per_day=rent_per_day,
            location=location
        )

        return redirect('my_equipment')

    return render(request,'add_equipment.html')


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def edit_equipment(request, id):

    equipment = get_object_or_404(Equipment, id=id)

    if request.method == "POST":
        equipment.name = request.POST['name']
        equipment.equipment_type = request.POST['equipment_type']
        equipment.description = request.POST['description']
        equipment.rent_per_day = request.POST['rent_per_day']
        equipment.location = request.POST['location']

        equipment.save()

        return redirect('my_equipment')

    return render(request, 'edit_equipment.html', {'equipment': equipment})

@login_required
def delete_equipment(request, id):

    equipment = get_object_or_404(Equipment, id=id)

    equipment.delete()

    return redirect('my_equipment')


@login_required
def rent_equipment(request, id):
    equipment = get_object_or_404(Equipment, id=id)

    RentalRequest.objects.create(
        buyer=request.user,
        equipment=equipment,
        start_date="2026-01-01",
        end_date="2026-01-02",
        status="Pending"
    )
    messages.success(request, "Rental request sent successfully!")

    return redirect('equipment_detail', id=id)

def rental_requests(request):
    supplier = request.user.supplier

    requests = RentalRequest.objects.filter(
        equipment__supplier=supplier
    ).order_by('-id')

    return render(request, 'rental_requests.html', {'requests': requests})



def approve_request(request, id):
    rental = get_object_or_404(RentalRequest, id=id)

    rental.status = "Approved"
    rental.equipment.available = False

    rental.equipment.save()
    rental.save()

    return redirect('rental_requests')


def reject_request(request, id):
    rental = get_object_or_404(RentalRequest, id=id)

    rental.status = "Rejected"
    rental.save()

    return redirect('rental_requests')


@login_required
def supplier_requests(request):
    supplier = Supplier.objects.get(user=request.user)

    requests = RentalRequest.objects.filter(
        equipment__supplier=supplier
    )

    return render(request, "supplier_requests.html", {"requests": requests})

@login_required
def supplier_profile(request):
    if not hasattr(request.user, 'supplier'):
        return redirect('home')

    supplier = request.user.supplier

    if request.method == "POST":
        supplier.company_name = request.POST.get('company_name')
        supplier.phone = request.POST.get('phone')
        supplier.address = request.POST.get('address')
        supplier.save()

        return redirect('supplier_dashboard')

    return render(request, 'supplier_profile.html', {
        'supplier': supplier
    })

@login_required
def my_requests(request):

    requests = RentalRequest.objects.filter(
        buyer=request.user
    ).order_by('-id')

    return render(request, 'my_requests.html', {
        'requests': requests
    })