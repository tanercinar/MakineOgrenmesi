# Makine Öğrenmesi ile Çalışan Deneyim Seviyesi Sınıflandırması
Bu proje makine öğrenmesi kullanarak "Dataset salary 2024" verisetindeki deneyim seviyelerini tahmin etmeye çalışmaktadır. Random Forest Classifier algoritması kullanılmıştır.
## Projenin Amacı
Projenin temel amacı, bir çalışanın maaşı, şirketin büyüklüğü, çalışma tipi gibi değişkenlere bakarak hangi kıdem seviyesinde (EN: Entry, MI: Mid, SE: Senior, EX: Executive) olduğunu sınıflandırmaktır.
## Uygulanan Yöntemler
Veri Temizleme ve Filtreleme:
Nadir görülen (veri setinin %2'sinden az) iş unvanları (job_title), modelin ezberlemesini (overfitting) önlemek amacıyla otherEN, otherSE gibi genel gruplar altında toplanmıştır.

### Veri Ön İşleme (Preprocessing):
Ordinal Encoding: Sıralı veri olan company_size (S < M < L) için uygulandı.
One-Hot Encoding: Sıralı olmayan kategorik veriler (job_title, employment_type vb.) için uygulandı.

### Pipeline Yapısı:
ColumnTransformer ve Pipeline kullanılarak veri işleme ve modelleme adımları tek bir akışta birleştirildi. Bu sayede veri sızıntısı (data leakage) engellendi.

### Model Eğitimi:
Algoritma: Random Forest Classifier
Eğitim/Test Oranı: %80 Eğitim, %20 Test

## Model performansı:
Bütün işlemeler sonucunda oluşturulan modelimiz %78 başarı oranı ile 'experience_level' sütununu tahmin ediyor. Başarı oranının bu seviyede olmasının sebebi ise görsellerden de anlaşılabileceği gibi veri setimizde 'experience_level' sütunundaki 'EN','EX' ve 'MI' değerlerinin az sayıda bulunmasıdır. Yeterince veri bulunan 'SE' değeri için alınan sonuçların başarı oranı model başarısından daha yüksektir. 'experience_level' sütununu tahmin etmek için en önemli özellik 'salary_in_usd' sütunudur, bu ikisi yüksek oranda korelasyon gösterir. 'employment_type' sütunuyla ise düşük oranda korelasyon gösterir.

<img width="773" height="443" alt="Screenshot 2025-11-25 at 09 44 11" src="https://github.com/user-attachments/assets/57660de1-efc4-4709-977d-ca8fda49844c" />


<img width="642" height="515" alt="Screenshot 2025-11-25 at 09 44 05" src="https://github.com/user-attachments/assets/ff983cc3-5546-4c5e-b330-4aca5d7ad591" />

<img width="752" height="461" alt="Screenshot 2025-11-25 at 09 43 46" src="https://github.com/user-attachments/assets/0fa6bef9-d908-4b08-a5da-3dbbe7fa4462" />

