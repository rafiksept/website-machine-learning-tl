from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from dashboard.models import JumlahKendaraan
import random
from datetime import datetime, timedelta


def landing_page(request):
    return render(request, 'landingpage.html' )

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
        #    print("ada")
            login(request, user)
            return redirect("dashboard")
        else:
            # print("tidak ada")
            render(request, "login.html")
    return render(request, "login.html")

@login_required(login_url="/login/")
def logout_user(request):
    logout(request)
    return redirect("landing_page")

def generate_data(request):
    jalan_value = ["Jalan Lingkar Selatan", "Jalan Berbudaya", "Jalan Hebat", "Jalan Unair"]
    jam_value = ["07.00 - 08.00", "12.00 - 13.00", "18.00 - 19.00"]
    jenis = ["motor","mobil"]

    # Mendapatkan tanggal saat ini
    # start_date = datetime.now() - timedelta(days=6)

    today = datetime.today().date()

    # Membuat daftar untuk menyimpan 7 tanggal terakhir
    last_seven_dates = []
    # last_seven_dates_chart = []

    # Menggunakan perulangan untuk menghasilkan 7 tanggal terakhir
    for i in range(7):
        # Menghitung tanggal sebelumnya
        previous_date = today - timedelta(days=i)
        # Menambahkan tanggal ke daftar
        last_seven_dates.append(previous_date)
    
    for i in last_seven_dates:
        for j in jalan_value:
            for k in jam_value:
                for s in jenis:
                    JumlahKendaraan.objects.create(
                    jalan=j,
                    jam=k,
                    jenis=s,
                    jumlah=random.randint(0, 500),
                    tanggal=i)
    
    return redirect("landing_page")