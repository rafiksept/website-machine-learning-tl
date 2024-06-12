from django.test import TestCase
from dashboard.models import JumlahKendaraan
import random
from datetime import datetime, timedelta

class JumlahKendaraanTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Buat 100 data dummy dengan field 'jalan' dan 'jam' tetap
        jalan_value = ["Jalan Lingkar Selatan", "Jalan Berbudaya", "Jalan Hebat", "Jalan Unair"]
        jam_value = ["07.00 - 08.00", "08.00 - 09.00", "09.00 - 10.00", "10.00 - 11.00"]
        jenis = ["motor","mobil"]

        # Mendapatkan tanggal saat ini
        today = datetime.now()

        # Menghitung tanggal 12 hari yang lalu
        twelve_days_ago = today - timedelta(days=12)

        # Menghasilkan tanggal acak antara twelve_days_ago dan today
        random_date = twelve_days_ago + timedelta(days=random.randint(0, 12))
        
        for i in range(100):
            JumlahKendaraan.objects.create(
                jalan=random.choice(jalan_value),
                jam=random.choice(jam_value),
                jenis=random.choice(jenis),
                jumlah=random.randint(0, 500),
                tanggal=random_date
            )

    def setUp(self):
        # Buat data dummy yang akan digunakan untuk setiap metode pengujian (jika diperlukan)
        pass

    def test_something(self):
        pass
