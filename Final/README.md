# Sertifikalar

Python Proramlama

<img width="855" height="598" alt="Screenshot 2026-01-20 at 22 21 56" src="https://github.com/user-attachments/assets/f61f532a-646a-423b-ba92-0f9abae4bc49" />

Python ile Makine Öğrenmesi Uygulamaları

<img width="855" height="598" alt="Screenshot 2026-01-20 at 22 21 30" src="https://github.com/user-attachments/assets/107ee9ce-f607-4064-a090-29a8df9acff4" />

# Akıllı Çöp Kutusu Doluluk Analizi ve Boşaltma Tahmini

Bu projenin amacı Smart_Bin.csv verisetini kullanarak konteynerlerin boşaltılması gerekip gerekmediğini tahmin etmektir. Proje konteyner türü, atık kategorisi ve çeşitli doluluk sensörü verilerini analiz ederek Emptying veya Non Emptying  kararını otomatik olarak verebilmektedir. Projede 5 farklı makine öğrenmesi modeli kullanılmış ve sonuçları karşılaştırılmıştır.

## Kodun Çalışma Mantığı

### 1. Gerekli Kütüphanelerin Eklenmesi

Veri işleme ve analizi için pandas makine öğrenmesi için sklearn görselleştirme için matplotlib ve seaborn kütüphanelerini kullandım.

### 2. Veri Setinin Yüklenmesi ve Temizlenmesi

Smart_Bin.csv dosyasını değişkene atadım ve "dropna()" metodu ile eksik değer içeren tüm satırlar veri setinden çıkardım.

### 3. Pivot Tablosu

Projede pivot tablo kullanarak çok fazla sayıda satırdan oluşan verisetindi daha kısa ve anlamlı bir parçaya dönüştürerek modelin hangi konteynır ve atık türü kombinasyonunun daha hızlı dolduğunu öğrenmesini ve daha iyi tahmin yapmasını sağladım.

<img width="851" height="44" alt="Screenshot 2026-01-20 at 22 15 21" src="https://github.com/user-attachments/assets/c82322b9-37c2-4cd0-b962-092f22d045c7" />

Pivot tabolunun konsol çıktıları:
<img width="413" height="453" alt="Screenshot 2026-01-20 at 22 34 15" src="https://github.com/user-attachments/assets/a1ff7e59-1623-47f1-91eb-48e0ede8e2c1" />
<img width="280" height="426" alt="Screenshot 2026-01-20 at 22 34 27" src="https://github.com/user-attachments/assets/188867b0-6784-4bf8-aa1c-4a8c6f4d2171" />


### 4. Veri Setindeki Gerekli Sütunların Sayısallaştırılması

Makine öğrenmesi modelleri sadece sayısal verilerle çalışabilir. Bu nedenden string değerlerli sütunları sayısal değerlere dönüştürdüm.

<img width="655" height="129" alt="Screenshot 2026-01-20 at 22 15 39" src="https://github.com/user-attachments/assets/f8aaddc3-2f7e-4229-8f55-d518dc4081b1" />



### 5. Üretilen Değerlerin Ana Tabloyla Birleştirilmesi

Pivot tablolarından elde edilen istatistiksel bilgiler ana veri setine yeni sütunlar olarak ekledim.

<img width="462" height="46" alt="Screenshot 2026-01-20 at 22 15 57" src="https://github.com/user-attachments/assets/9e404c26-3bd9-4fc0-9472-538fc612fd25" />


### 6. Modelin Hazırlanması ve Verinin Bölünmesi

Hedef Değişken:Class
Özellikler:FL_B, FL_A, VS, FL_B_3, FL_A_3, FL_B_12, FL_A_12, Container Type Encoded, Recyclable fraction Encoded, avg_FL_B, avg_FL_A

Ölçeklendirme: Özellikler farklı aralıklarda olduğu için daha tutarlı sonuçlar almak için StandardScaler ile ölçeklendirme yaptım.

Veriyi %80 eğitim %20 test olacak şekilde böldüm.

### 7. Modellerin Eğitilmesi ve Karşılaştırılması

<img width="690" height="415" alt="Screenshot 2026-01-20 at 22 16 29" src="https://github.com/user-attachments/assets/06e77274-1545-488d-bdb2-80669998c10a" />

5 farklı makine öğrenmesi algoritması kullanarak eğitim yaptım ve sonuçları karşılaştırdım.

#### Model Sonuçları:

| Model | Doğruluk Oranı |
|-------|----------------|
| Random Forest | %95.7 |
| Decision Tree | %93.9 |
| Gradient Boosting | %92.9 |
| KNN Classification | %89.9 |
| Logistic Regression | %89.3 |

Random Forest modeli %95.7 doğruluk oranıyla en başarılı sonucu vermiştir.


### 8. Görselleştirmeler

#### Grafik 1: Confusion Matrix (Karmaşıklık Matrisi)

<img width="3772" height="2068" alt="plot1" src="https://github.com/user-attachments/assets/673c196f-4fc0-4bca-ab8f-ee0e39b0f9a8" />

#### Grafik 2: Model Karşılaştırması

<img width="4169" height="2068" alt="plot2" src="https://github.com/user-attachments/assets/93dd0a61-f464-4452-8c8c-b53b5664f0f1" />


#### Grafik 3: Feature Importance Tablosu

<img width="3569" height="2669" alt="plot3" src="https://github.com/user-attachments/assets/cfb215d8-400b-4dcb-8f8d-eb4684478dbd" />

## Sonuç

Bu projede makine öğrenmesi modelleri kullanarak çöp kutularının etkin yönetimini sağlayan bir sistem geliştirilmiştir. Random Forest modeli ile %95.7 doğruluk oranı elde edilerek sistemin gerçek hayatta kullanılabilir seviyede olduğu kanıtlanmıştır. Pivot tablolar sayesinde veri daha anlamlı bilgilere dönüştürülmüş ve model performansı artırılmıştır.
