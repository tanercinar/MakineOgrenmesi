# Makine Öğrenmesi ile Çalışan Deneyim Seviyesi Sınıflandırması
Bu proje makine öğrenmesi kullanarak belirli meslek gruplarındaki çalışanların verilerini kullanarak maaş ve deneyim seviyesi tahmini yapılmaya çalışılmaktadır. Regresyon ile maaş tahmini ve Random Forest ile deneyim seviyesi tahmini olarak iki farklı yaklaşım denenmiş ve verisetinin bu yaklaşımlara uygunluğu karşılaştırılmıştır.

# 1. Veri Setinin Eğitime Hazırlanması
Maaş tahmini için: 'work_year', 'experience_level', 'employment_type', 'job_title','remote_ratio', 'company_location', 'company_size' sütunları kullanılırken, deneyim seviyesi tahmini için ise 'work_year', 'employment_type', 'job_title','salary_in_usd','remote_ratio', 'company_location', 'company_size' sütunları kullanılmıştır.

### Verinin filtrelenmesi
Veride bulunan 'job_title' sütununda çok fazla sayıda az sayıda bulunan değer olduğu tespit edilmiş, öğrenememeye yol açmaması için önce bu satırların çıkarılmaları denenmiş ancak bunun da veri setinin büyük kısmının atılmasına, bunun sonucu olarak da zaten az değer bulunan bazı değerler için('experience_level' sütununun EN ve EX değerleri) öğrenememeye yol açtığı görülmüş ve bu doğrultuda az görülen unvanlar 'other' adı altında tek bir çatıda toplanmıştır.

### Kategorik Dönüşüm
Ordinal Encoding: Sıralı veri içeren experience_level (EN < MI < SE < EX) ve company_size (S < M < L) sütunları sıralı olarak sayısal değerlere dönüştürülmüştür.

One-Hot Encoding: Sıralı olmayan job_title, employment_type gibi nominal veriler 0 ve 1 değerlerine çevrilmiştir.

### Eğitim ve Test verilerinin ayırma
Bu işlemler sonucunda eğitime hazır hale getirilen verisetinin %80'i eğitim %20'si de test için ayırılmıştır.

# 2. Maaş Tahmin Modeli
Filtrelenmiş ve kategorik dönüşümleri yapılmış veri üzerinde 12 farklı model denenmiştir, sonuçlar aşağıdaki tabloda bulunmaktadır. En iyi sonucu Random Forest modeli verse de bu model başarılı olmaktan çok uzaktadır ve yapılan işlemlere rağmen bu sonuncun alınmasından dolayı bu verisetinin maaş(salary_in_usd) tahmini yapmaya uygun olmadığı sonucuna varılarak farklı bir target sutun seçilmiştir.

| Model | R² Score | Ortalama Hata (MAE) |
| :--- | :--- | :--- |
| **Random Forest** | **0.3017** | **$41,297** |
| Ridge Regressor | 0.2973 | $41,488 |
| Gradient Boosting | 0.2968 | $41,782 |
| Linear Regression | 0.2963 | $41,512 |
| SGD Regressor | 0.2954 | $41,734 |
| Bagging Regressor | 0.2945 | $41,495 |
| Extra Trees | 0.2797 | $41,853 |
| Passive Aggressive | 0.2767 | $41,277 |
| Extra Tree | 0.2750 | $41,986 |
| Decision Tree | 0.2725 | $42,058 |
| K-Neighbors (KNN) | 0.2136 | $43,825 |
| AdaBoost | 0.1572 | $47,738 |

# 3. Deneyim Seviyesi Tahmin Modeli
Maaş tahmininde istenilen sonucun elde edilememesi üzerine deneyim(experience_level) tahminine yönenilmiş ve 15 farklı model denenmiştir, sonuçlar aşağıdaki tabloda bulunmaktadır. En başarılı sonuç %69.58 başarı oranı ile Gradient Boosting metoduyla yapılan modele aittir.

| Model | Doğruluk Oranı (Accuracy) |
| :--- | :--- |
| **Gradient Boosting** | **0.69580** |
| **Bagging Classifier** | **0.69066** |
| **Random Forest** | **0.69066** |
| Extra Trees | 0.68793 |
| Extra Tree | 0.67705 |
| Decision Tree | 0.67342 |
| AdaBoost | 0.66223 |
| K-Neighbors (KNN) | 0.65951 |
| Ridge Classifier | 0.65588 |
| Logistic Regression | 0.65558 |
| MLP Classifier | 0.65558 |
| Bernoulli NB | 0.64802 |
| Nearest Centroid | 0.24826 |
| SGD Classifier | 0.07711 |
| Passive Aggressive | 0.07711 |

# 4. Sonuç ve Çıkarımlar
Yapılan işlemler sonucunda eldeki verisetinin sayısal değerlerden oluşan 'salary_in_usd' sütunundansa kategorik değerler içeren 'experience_level' sütununu tahmin etmeye daha elverişli olduğu görülmüştür. Regresyon ile maaş tahmin modeli düşük bir R skoru elde edip maaşın değerini verideki değer sütunlarla açıklamada yetersiz kalırken, deneyim seviyesi tahmini için Gradient Boosting algoritması ile oluşturulan model %69 gibi bir doğruluk oranı elde edip çok daha başarılı olmuştur.
Aradaki bu büyük farkın temel nedeni maaşın, elimizdeki veride bulunmayan bir çok dış etkene de bağlı olmasıdır. Deneyim düzeyi ise en aşağıda eklenen tabloya da bakacak olursak maaş ile doğrudan orantılıdır ve yüksek korelasyon gösterir. Bu nedenle maaşın hedef değil de bir feature olarak kullanıldığı bir model çok daha tutarlı sonuçlar vermiştir.
### Algoritmaların Karşılaştırmaları
Algoritmalar arasında yapılan karşılaştırmada hem regresyon hem de sınıflandırma görevlerinde ağaç tabanlı modellerin (Random Forest ve Gradient Boosting) doğrusal modellere (Linear ve Logistic Regression) kıyasla daha yüksek performans verdiği gözlemlenmiştir. Bu durum, veri setindeki özellikler ile hedef değişkenler arasındaki ilişkinin doğrusal olmaktan ziyade daha karmaşık ve hiyerarşik bir yapıda olduğunu kanıtlamaktadır. Dolayısıyla bu tip veri setlerinde karmaşık ilişkileri modelleyebilen algoritmaların tercih edilmesi gerekmektedir.
### Veri Dengesizliğinin Sonuca Etkisi
Modelin sonucundan oluşturulan hit/miss grafiğinden de görülebileceği gibi veri dengesizliğinden dolayı model, az sayıda bulunan 'EX' ve 'EN' değerlerini tahmin ederken düşük başarı göstermiş, en yüksek sayıda verinin bulunduğu 'SE' değerini tahmin ederken ise en yüksek başarı oranını göstermiştir.
### Genel Değerlendirme
Oluşturulan modeller sonucunda başarılı bir maaş tahmini yapılamazken, başarılı sayılabilecek vir deneyim seviyesi tahmini yapılabilmektedir. Eldeki gürültülü veri ile, uygulanan filtreleme ve gruplandırma işlemlerinin de yardımı ile %78 gibi bir oranla tahmin yapan bir model eğitilmiş verinin yapısal özelliklerinin regresyon yerine sınıflandırma problemlerine daha uygun olduğu ortaya konmuştur.

<img width="758" height="476" alt="Screenshot 2025-11-25 at 09 43 41" src="https://github.com/user-attachments/assets/27488e7f-4b98-4a79-912a-6536423380e0" />

Gradient Boosting Algoritmasıyla Eğitilen Modelin Filtresiz Hit/Miss Grafiği

<img width="773" height="443" alt="Screenshot 2025-11-25 at 09 44 11" src="https://github.com/user-attachments/assets/57660de1-efc4-4709-977d-ca8fda49844c" />

Gradient Boosting Algoritmasıyla Eğitilen Modelin Filtreleme Sonrası Hit/Miss Grafiği

<img width="642" height="515" alt="Screenshot 2025-11-25 at 09 44 05" src="https://github.com/user-attachments/assets/ff983cc3-5546-4c5e-b330-4aca5d7ad591" />

Filtrelenmiş Verinin Confusion Matrisi

<img width="989" height="590" alt="output" src="https://github.com/user-attachments/assets/69a28562-babc-48eb-a7e3-31b49037bd24" />

'experience_level' Hedef Sütununun Korelasyon Grafiği

