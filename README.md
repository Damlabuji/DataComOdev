VERI HABERLESMESI ODEVI – HATA TESPIT YONTEMLERI SIMULASYONU

Bu proje Veri Haberlesmesi (Data Communications) dersi kapsaminda hazirlanmis bir odevdir. Projenin amaci, veri iletimi sirasinda olusabilecek hatalari ve bu hatalarin farkli hata tespit yontemleri kullanilarak nasil algilandigini uygulamali olarak gostermektir.

Proje Python dili ile gelistirilmistir ve istemci–sunucu (client–server) mimarisi kullanilmistir. Gercek bir ag iletisimine benzer sekilde, gonderilen verinin bir kanal uzerinden gecerek aliciya ulasmasi saglanmistir.

SISTEM MIMARISI
Sistem uc ana bilesenden olusmaktadir:

Gonderici (Sender) -> Sunucu (Kanal) -> Alici (Receiver)

Bu yapi, derslerde anlatilan gurultulu kanal kavramini temsil etmektedir.

GONDERICI (sender.py)
Gonderici tarafi kullanici ile etkilesimlidir.

Gorevleri:

* Kullanicidan metin verisini almak
* Kullanicinin sectigi hata tespit yontemine gore kontrol bilgisi uretmek
* Veriyi "VERI | YONTEM | KONTROL_BILGISI" formatinda sunucuya gondermek

Desteklenen hata tespit yontemleri:

* Cift Parite Biti (Even Parity)
* Iki Boyutlu Parite (2D Parity)
* CRC-16
* Internet Checksum

SUNUCU (server.py)
Sunucu, sistemde iletisim kanali gorevini ustlenmektedir.

Gorevleri:

* Once aliciyi, ardindan gondericiyi baglamak
* Gondericiden gelen veriyi almak
* Veri uzerinde bilinclı olarak hata olusturmak
* Bozulmus veriyi aliciya iletmek

Uygulanan hata turleri:

* Bit degistirme (bit flip)
* Karakter degistirme
* Karakter silme
* Karakter ekleme
* Karakterlerin yerini degistirme
* Burst error (ardisik hata)

ALICI (receiver.py)
Alici tarafi, iletilen verinin dogrulugunu kontrol eder.

Gorevleri:

* Sunucudan gelen paketi almak
* Paketi guvenli sekilde ayristirmak
* Secilen yonteme gore kontrol bilgisini yeniden hesaplamak
* Gelen kontrol bilgisi ile hesaplanan degeri karsilastirmak

Sonuclar:

* DATA CORRECT: Veri dogru, hata tespit edilmedi
* DATA CORRUPTED: Veri bozulmus, hata tespit edildi

YARDIMCI MODUL (protocol_utils.py)
Bu dosya hata tespit ve hata olusturma islemlerini icermektedir.

ErrorDetector sinifi:

* Parite biti hesaplama
* Iki boyutlu parite
* CRC-16
* Internet checksum
* Basitlestirilmis hamming (ornek amacli)

DataCorruptor sinifi:

* Sunucu tarafinda veriyi bozan hata turlerini icerir

PROJENIN CALISTIRILMASI
Dosyalar farkli terminallerde asagidaki sirayla calistirilmalidir:

1. python server.py
2. python receiver.py
3. python sender.py

Gonderici tarafindan metin girilip yontem secildiginde, sonuclar alici ekraninda goruntulenir.

PROJENIN AMACI
Bu proje ile veri haberlesmesinde hata kavrami pekistirilmis, farkli hata tespit yontemlerinin etkinligi gozlemlenmis ve teorik bilgilerin pratikte uygulanmasi saglanmistir.

HAZIRLAYANLAR
2310205027 Yiğit Başoğlu
2510205402 Şevval Ateş

Karabuk Universitesi
Bilgisayar Muhendisligi Bolumu
