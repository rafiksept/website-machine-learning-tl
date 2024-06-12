from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import JumlahKendaraan
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from datetime import date
from collections import defaultdict
from dashboard.webster import Webster
import json
import locale
# import math

# from myapp.models import MyModel  # Sesuaikan dengan nama model Anda

@login_required(login_url="/login/")
def dashboard(request):

    today = datetime.today().date()
    # print(today)
    kendaraanHariIni = JumlahKendaraan.objects.filter(tanggal=today).aggregate(total=Sum('jumlah'))
    # Mengakses nilai total
    jumlahKendaraanHariIni = kendaraanHariIni['total'] if kendaraanHariIni['total'] is not None else 0
    kemarin = helper_date_web()
    rentang_waktu = helper_date_interval()
    

        # Menghitung tanggal tujuh hari yang lalu
    start_date = datetime.now() - timedelta(days=6)

    # today = datetime.today().date()

    # Membuat daftar untuk menyimpan 7 tanggal terakhir
    last_seven_dates = []
    last_seven_dates_chart = []

    # Menggunakan perulangan untuk menghasilkan 7 tanggal terakhir
    for i in range(7):
        # Menghitung tanggal sebelumnya
        previous_date = today - timedelta(days=i)
        # Menambahkan tanggal ke daftar
        last_seven_dates.append(previous_date.strftime('%d'))
        last_seven_dates_chart.append(previous_date.strftime('%d %b'))

    last_seven_dates = sorted(last_seven_dates)
    last_seven_dates_chart = sorted(last_seven_dates_chart)
    # print(last_seven_dates)

    # Menyimpan data dalam variabel
    hasil_query = JumlahKendaraan.objects.filter(tanggal__gte=start_date).values('tanggal', 'jenis').annotate(jumlahKendaraan=Sum('jumlah')).order_by('tanggal', 'jenis')

    data_terakhir_tujuh_mobil = dict()
    data_terakhir_tujuh_motor = dict()
    # Menampilkan hasil
    for item in hasil_query:
        if item["jenis"] == "mobil":
            data_terakhir_tujuh_mobil[item["tanggal"].strftime('%d')] = {
                "jumlahKendaraan" : item["jumlahKendaraan"],
            }
        else :
            data_terakhir_tujuh_motor[item["tanggal"].strftime('%d')] = {
                "jumlahKendaraan" : item["jumlahKendaraan"],
            }

    datamobil7  = []

    for i in last_seven_dates:
        if i not in data_terakhir_tujuh_mobil.keys():
           
            datamobil7.append({
            "x" : i,
            "y" : 0 
            }
            )
        else : 
            datamobil7.append({
                "x" : i,
                "y" : data_terakhir_tujuh_mobil[i]["jumlahKendaraan"]
            })

    datamotor7  = []
    
    
   
    for i in last_seven_dates:
        if i not in data_terakhir_tujuh_motor.keys():
            datamotor7.append({
            "x" : i,
            "y" : 0 
            }
            )
        else : 
            datamotor7.append({
                "x" : i,
                "y" : data_terakhir_tujuh_motor[i]["jumlahKendaraan"]
            })

    list_data_mobil = []
    for i in datamobil7:
        list_data_mobil.append(i["y"])

    list_data_motor = []
    for i in datamotor7:
        list_data_motor.append(i["y"])

    tujuh_hari_terakhir = timezone.now().date() - timedelta(days=6)
    data_kemarin = list_data_mobil[-2] + list_data_motor[-2] 
    # print(list_data_mobil)

    perubahan = ((jumlahKendaraanHariIni - data_kemarin)/data_kemarin) * 100
 


    # Tempat Terpadat
    data_tempat = JumlahKendaraan.objects.filter(tanggal__gte=tujuh_hari_terakhir).values('jalan').annotate(total_kendaraan=Sum('jumlah')).order_by('-total_kendaraan')[:5]
    data_waktu = JumlahKendaraan.objects.filter(tanggal__gte=tujuh_hari_terakhir).values('jam').annotate(total_kendaraan=Sum('jumlah')).order_by('-total_kendaraan')[:5]

    # print(data_waktu)
    pagi=["06.00 - 07.00", "07.00 - 08.00", "08.00 - 09.00", "09.00 - 10.00", "10.00 - 11.00", "11.00 - 12.00"]
    siang=["12.00 - 13.00", "13.00 - 14.00", "14.00 - 15.00", "15.00 - 16.00", "16.00 - 17.00", "17.00 - 18.00"]
    malam=["18.00 - 19.00", "19.00 - 20.00", "20.00 - 21.00", "21.00 - 22.00", "22.00 - 23.00", "23.00 - 24.00"]

    total_jumlah_kendaraan_pagi = JumlahKendaraan.objects.filter(jam__in=pagi).filter(tanggal__gte=tujuh_hari_terakhir).aggregate(total=Sum('jumlah'))
    total_jumlah_kendaraan_siang = JumlahKendaraan.objects.filter(jam__in=siang).filter(tanggal__gte=tujuh_hari_terakhir).aggregate(total=Sum('jumlah'))
    total_jumlah_kendaraan_malam = JumlahKendaraan.objects.filter(jam__in=malam).filter(tanggal__gte=tujuh_hari_terakhir).aggregate(total=Sum('jumlah'))
    # print(total_jumlah_kendaraan_pagi)

    
    if total_jumlah_kendaraan_siang["total"] is None:
        total_siang = 0
    else :
        total_siang = total_jumlah_kendaraan_siang["total"]
    
    if total_jumlah_kendaraan_pagi["total"] is None:
        total_pagi = 0
    else : 
        total_pagi = total_jumlah_kendaraan_pagi["total"]

    if total_jumlah_kendaraan_malam["total"] is None:
        total_malam = 0
    else :
        total_malam = total_jumlah_kendaraan_malam["total"]

    total_donut = total_siang + total_pagi + total_malam

    # print(total_jumlah_kendaraan_siang)
    # print(data)

    context = {
        "dashboard" : "dashboard",
        "jumlahKendaraan" : intcomma(jumlahKendaraanHariIni),
        "kemarin" : kemarin,
        "rentang_waktu" : rentang_waktu,
        "mobil_bar_chart" : json.dumps(datamobil7),
        "motor_bar_chart" : json.dumps(datamotor7),
        'motor_line_chart' : json.dumps(list_data_motor),
        'mobil_line_chart' : json.dumps(list_data_mobil),
        'date_line_chart' : json.dumps(last_seven_dates_chart),
        'data_tempat' : data_tempat,
        'data_waktu' : data_waktu,
        'pagi_data': json.dumps(total_pagi),
        'siang_data': json.dumps(total_siang),
        'malam_data': json.dumps(total_malam),
        'total_donut': json.dumps(intcomma(total_donut)),
        'perubahan' : round(perubahan, 2)
    }
    return render(request, 'dashboard.html' , context)

@login_required(login_url="/login/")
def data_page(request):
    today = datetime.today().date()
    jalan = request.GET.get('jalan', 'Tidak ada nilai')
    tanggal = request.GET.get('tanggal', 'Tidak ada nilai')

    if jalan == 'Tidak ada nilai' :
        jalan = "Jalan Lingkar Selatan"

    if tanggal == 'Tidak ada nilai' :
        tanggal = today

    # print(tanggal)

    # print(jalan)
    jumlah_kendaraan_mobil = JumlahKendaraan.objects.filter(tanggal=tanggal).filter(jenis="mobil").filter(jalan=jalan)
    jumlah_kendaraan_motor = JumlahKendaraan.objects.filter(tanggal=tanggal).filter(jenis="motor").filter(jalan=jalan)
    context = {
        "dashboard":"data",
        "jumlah_kendaraan_mobil" : jumlah_kendaraan_mobil,
        "jumlah_kendaraan_motor" : jumlah_kendaraan_motor,
        'jalan' : jalan,
        'tanggal' : tanggal
    }

    return render(request, 'data.html', context)

@login_required(login_url="/login/")
def perhitungan(request):
    today = datetime.today().date()
    semua_kendaraan = []
    total_smp = []

    tanggal = request.GET.get('tanggal', 'Tidak ada nilai')

    if tanggal == 'Tidak ada nilai' :
        tanggal = today
    
    # semua_kendaraan_motor = dict()
    jalan = ["Jalan Lingkar Selatan", "Jalan Berbudaya","Jalan Hebat","Jalan Unair"]

    for i in jalan:
        jumlah_kendaraan_mobil = JumlahKendaraan.objects.filter(tanggal=tanggal).filter(jenis="mobil").filter(jalan=i)
        jumlah_kendaraan_motor = JumlahKendaraan.objects.filter(tanggal=tanggal).filter(jenis="motor").filter(jalan=i)

    
        jmotor = []
        for j in jumlah_kendaraan_motor:
            jmotor.append(j.jumlah)
          
        



        smp_mobil = []
        for k in jumlah_kendaraan_mobil:
            smp_mobil.append(k.jumlah)

        print(smp_mobil)



            # Mengalikan setiap elemen dalam list dengan 0.2
        smp_motor = [round(elemen * 0.2, 2) for elemen in jmotor]



        jumlah_kendaraan = [x + y for x, y in zip(jmotor, smp_mobil)]


        jumlah_smp = [x + y for x, y in zip(smp_motor, smp_mobil)]

    
        semua_kendaraan.append(zip(jumlah_kendaraan_mobil, jumlah_kendaraan_motor, smp_mobil, smp_motor, jumlah_kendaraan, jumlah_smp))
        total_smp.append(jumlah_smp)


        # Mengelompokkan elemen-elemen sesuai dengan indeks

    
    total_smp_jam = [[row[i] for row in total_smp] for i in range(len(total_smp[0]))]

    jam = request.GET.get('jam', 'Tidak ada nilai')

    if jam == 'Tidak ada nilai' or jam == "07.00 - 08.00" :
        jam = "07.00 - 08.00"
        jam_index = 0
    elif jam == "12.00 - 13.00":
        jam_index = 1
    elif jam == "18.00 - 19.00":
        jam_index = 2



    try : 
        webster = Webster()
        arus_jenuh_kendaraan = webster.arus_tiap_persm()
        tingkat_arus, Y = webster.tingkat_arus_lalu_lintas(total_smp_jam[jam_index], arus_jenuh_kendaraan)
        L = webster.waktu_hilang_total(webster.waktu_hilang)
        CO = webster.siklus_optimum(L, Y)
        waktu_hijau_maksimum = webster.waktu_hijau_maks(CO, L)
        hijau_list_maksimum = webster.calc_waktu_hijau_efektif(waktu_hijau_maksimum, Y, tingkat_arus)
        merah_list_maksimum = webster.calc_lampu_merah_efektif(CO, hijau_list_maksimum, webster.waktu_hilang)
    except : 
        context = {
            "error" : True
        }
        return render(request, 'perhitungan.html', context)


    # print(semua_kendaraan)

    


    context = {
        "dashboard" : "perhitungan",
        "semua_kendaraan" : zip(jalan, semua_kendaraan),
        "waktu_hilang" : webster.waktu_hilang,
        "arus_jenuh" : zip(jalan, arus_jenuh_kendaraan),
        "tingkat_arus" : zip(range(0, len(tingkat_arus)), tingkat_arus),
        "Y" :Y,
        "L" : L,
        "CO" :CO,
        "waktu_hijau_maksimum" : waktu_hijau_maksimum,
        "hijau_list_maksimum" :zip(jalan, hijau_list_maksimum),
        "merah_list_maksimum" : zip(jalan, merah_list_maksimum),
        "tabel_hasil" : zip(jalan, merah_list_maksimum, hijau_list_maksimum),
        "jam" : jam,
        "tanggal" : tanggal
       
    }
    return render(request, 'perhitungan.html', context)




def helper_date_web():
        # Set locale untuk memastikan nama bulan dalam bahasa Indonesia
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    # Dapatkan tanggal hari ini
    today = datetime.now()

    # Kurangi satu hari untuk mendapatkan tanggal kemarin
    yesterday = today - timedelta(days=1)

    # Format tanggal kemarin sesuai yang diinginkan
    formatted_yesterday = yesterday.strftime('%d %B %Y')

    return formatted_yesterday

def helper_date_interval():
    # Set locale untuk memastikan nama bulan dalam bahasa Indonesia
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    # Dapatkan tanggal hari ini
    today = datetime.now()

    # Tentukan tanggal 7 hari yang lalu
    start_date = today - timedelta(days=6)

    # Format tanggal mulai dan tanggal hari ini
    formatted_start_date = start_date.strftime('%d %B')
    formatted_today = today.strftime('%d %B, %Y')

    # Gabungkan format tanggal menjadi satu string
    formatted_range = f"{formatted_start_date} - {formatted_today}"

    return formatted_range