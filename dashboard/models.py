from django.db import models

class JumlahKendaraan(models.Model):
    jalan = models.CharField(max_length=100)
    jam = models.CharField(max_length=100)
    tanggal = models.DateField()
    jumlah = models.IntegerField()
    jenis = models.CharField(max_length=100)
    path_video = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
