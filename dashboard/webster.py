import math
class Webster:
    def __init__(self) -> None:
        self.waktu_hilang = 5
        self.l_jalan = [6, 4, 4.5, 4]
        self.n = 4

    def arus_jenuh(self, lebar_jalan):
        return lebar_jalan * 525
    
    def arus_tiap_persm(self):
        arus_jenuh_tiap_persimpangan = [self.arus_jenuh(lebar) for lebar in self.l_jalan]
        return arus_jenuh_tiap_persimpangan


    def tingkat_arus(self, total_smp, arus_jenuh_tiap_persimpangan):
        tingkat_arus_per_persimpangan = [
            smp / arus_jenuh
            for smp, arus_jenuh in zip(total_smp, arus_jenuh_tiap_persimpangan)
        ]
        return tingkat_arus_per_persimpangan
    
    def tingkat_arus_lalu_lintas(self, total_smp, arus_jenuh_tiap_persimpangan):
        tingkat_arus_per_persimpangan = self.tingkat_arus(total_smp, arus_jenuh_tiap_persimpangan)
        tingkat_arus_per_persimpangan = [round(y, 4) for y in tingkat_arus_per_persimpangan]

        Y = sum(tingkat_arus_per_persimpangan)
        return tingkat_arus_per_persimpangan, Y


    def waktu_hilang_total(self, R):
        L = 2*self.n + R
        return L

    # C0 = waktu siklus optimum (detik)
    # L = waktu hilang total per siklus
    # Y = jumlah y maksimum untuk semua fase

    def siklus_optimum(self, L, Y):
        C0 = (1.5*L+5)/(1-Y)
        return math.floor(C0)
    
    def waktu_hijau_maks(self, C0,L):
        hijau_maks = C0 - L
        return hijau_maks
    
    def waktu_hijau_efektif(self, y, waktu_hijau_maks, Y):
        g = (y * waktu_hijau_maks) / Y
        return math.ceil(g)
    
    def calc_waktu_hijau_efektif(self, hijau_maks, Y, tingkat_arus_per_persimpangan):
        waktu_hijau_efektif_per_persimpangan = [
            self.waktu_hijau_efektif(y, hijau_maks, Y)
            for y in tingkat_arus_per_persimpangan]
        
        return waktu_hijau_efektif_per_persimpangan
    
    def fase(self, C0, hijau_maks, waktu_kuning):
        return C0 - hijau_maks - waktu_kuning
    
    def calc_lampu_merah_efektif(self, C0, hijau_maks, R):
        fase_per_persimpangan = [
            self.fase(C0, waktu_hijau_efektif, R)
            for waktu_hijau_efektif in hijau_maks
        ]
        return fase_per_persimpangan