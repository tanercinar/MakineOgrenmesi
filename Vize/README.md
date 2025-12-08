# Makine Öğrenmesi ile Çalışan Deneyim Seviyesi Sınıflandırması
Bu proje makine öğrenmesi kullanarak belirli meslek gruplarındaki çalışanların verilerini kullanarak maaş ve deneyim seviyesi tahmini yapılmaya çalışılmaktadır. Regresyon ile maaş tahmini ve Random Forest ile deneyim seviyesi tahmini olarak iki farklı yaklaşım denenmiş ve verisetinin bu yaklaşımlara uygunluğu karşılaştırılmıştır.

# 1. Veri Setinin Eğitime Hazırlanması
Maaş tahmini için: 'work_year', 'experience_level', 'employment_type', 'job_title','remote_ratio', 'company_location', 'company_size' sütunları kullanılırken, deneyim seviyesi tahmini için ise 'work_year', 'employment_type', 'job_title','salary_in_usd','remote_ratio', 'company_location', 'company_size' sütunları kullanılmıştır. Her iki tahmin için de 'salary', 'salary_currency' ve 'employee_residence' sütunları kullanılmamıştır. 'employee_residence' sütununun maaş ve deneyim seviyesi tahmini için, özellikle de verinin içinde benzer bir feature olup da daha büyük önem taşıyan bir 'company_location' sütunu da bulunduğundan dolayı gereksiz olmasından dolayı kullanılmamıştır. 'salary' ve 'salary_currency' sütunları ise 'salary_in_usd' sütununun bu iki sütunun birleşiminden oluşmasından dolayı sadece o feature veya target olarak alımıştır.

### Verisetinin İlk 5 Satırı
| | work_year | experience_level | employment_type | job_title | salary | salary_currency | salary_in_usd | employee_residence | remote_ratio | company_location | company_size |
|---:|---:|:---|:---|:---|---:|:---|---:|:---|---:|:---|:---|
| 0 | 2024 | SE | FT | AI Engineer | 202730 | USD | 202730 | US | 0 | US | M |
| 1 | 2024 | SE | FT | AI Engineer | 92118 | USD | 92118 | US | 0 | US | M |
| 2 | 2024 | SE | FT | Data Engineer | 130500 | USD | 130500 | US | 0 | US | M |
| 3 | 2024 | SE | FT | Data Engineer | 96000 | USD | 96000 | US | 0 | US | M |
| 4 | 2024 | SE | FT | Machine Learning Engineer | 190000 | USD | 190000 | US | 0 | US | M |


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

<img width="1000" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/2e1001d1-a95e-4a4b-886c-26e217803391" />


# 3. Deneyim Seviyesi Tahmin Modeli
Maaş tahmininde istenilen sonucun elde edilememesi üzerine deneyim(experience_level) tahminine yönenilmiş ve 14 farklı model denenmiştir, sonuçlar aşağıdaki tabloda bulunmaktadır. En başarılı sonuç %70.27 başarı oranı ile Random Forest metoduyla yapılan modele aittir.

| Model | Doğruluk (Accuracy) |
| :--- | :--- |
| Logistic Regression | 0.65558 |
| Ridge Classifier | 0.65588 |
| SGD Classifier | 0.07711 |
| Passive Aggressive | 0.07711 |
| K-Neighbors (KNN) | 0.66102 |
| Nearest Centroid | 0.24826 |
| Decision Tree | 0.67735 |
| Extra Tree | 0.69005 |
| AdaBoost | 0.65921 |
| Bagging Classifier | 0.69701 |
| Bernoulli NB | 0.65891 |
| MLP Classifier | 0.65558 |
| **Random Forest** | **0.70275** |
| Gradient Boosting | 0.69791 |

# 4. Sonuç ve Çıkarımlar
Yapılan işlemler sonucunda eldeki verisetinin sayısal değerlerden oluşan 'salary_in_usd' sütunundansa kategorik değerler içeren 'experience_level' sütununu tahmin etmeye daha elverişli olduğu görülmüştür. Maaş tahmin modeli düşük bir R skoru elde edip maaşın değerini verideki değer sütunlarla açıklamada yetersiz kalırken, deneyim seviyesi tahmini için Random Forest algoritması ile oluşturulan model %70 gibi bir doğruluk oranı elde edip çok daha başarılı olmuştur.
Aradaki bu büyük farkın temel nedeni maaşın, elimizdeki veride bulunmayan bir çok dış etkene de bağlı olmasıdır. Deneyim düzeyi ise en aşağıda eklenen tabloya da bakacak olursak maaş ile doğrudan orantılıdır ve yüksek korelasyon gösterir. Bu nedenle maaşın hedef değil de bir feature olarak kullanıldığı bir model çok daha tutarlı sonuçlar vermiştir.
### Algoritmaların Karşılaştırmaları
Algoritmalar arasında yapılan karşılaştırmada hem regresyon hem de sınıflandırma görevlerinde ağaç tabanlı modellerin (Random Forest ve Gradient Boosting) doğrusal modellere (Linear ve Logistic Regression) kıyasla daha yüksek performans verdiği gözlemlenmiştir. Bu durum, veri setindeki özellikler ile hedef değişkenler arasındaki ilişkinin doğrusal olmaktan ziyade daha karmaşık ve hiyerarşik bir yapıda olduğunu kanıtlamaktadır. Dolayısıyla bu tip veri setlerinde karmaşık ilişkileri modelleyebilen algoritmaların tercih edilmesi gerekmektedir.
### Veri Dengesizliğinin Sonuca Etkisi
Modelin sonucundan oluşturulan hit/miss grafiğinden de görülebileceği gibi veri dengesizliğinden dolayı model, az sayıda bulunan 'EX' ve 'EN' değerlerini tahmin ederken düşük başarı göstermiş, en yüksek sayıda verinin bulunduğu 'SE' değerini tahmin ederken ise en yüksek başarı oranını göstermiştir. Bunun önüne geçmek için en iyi başarı oranı veren Random Forest modeline class_weight='balanced' parametresi verilmiş ancak bunun başarı oranını düşürdüğü görülerek kullanılmamasına karar verilmiştir.
### Genel Değerlendirme
Oluşturulan modeller sonucunda başarılı bir maaş tahmini yapılamazken, başarılı sayılabilecek bir deneyim seviyesi tahmini yapılabilmektedir. Eldeki gürültülü veri ile, uygulanan filtreleme ve gruplandırma işlemlerinin de yardımı ile %70 gibi bir oranla tahmin yapan bir model eğitilmiş verinin yapısal özelliklerinin regresyon yerine sınıflandırma problemlerine daha uygun olduğu ortaya konmuştur.


<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/96d2cd20-5d16-40ec-a155-9cb1dc6bde2d" />

Random Forest Algoritmasıyla Eğitilen Modelin Hit/Miss Grafiği

<img width="526" height="453" alt="image" src="https://github.com/user-attachments/assets/3b6ee8de-cde5-4032-a1a4-d9c0bae17b8b" />


Modelin Karmaşıklık Matrisi

<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/cd6d1f4d-38cf-4404-9353-4e0ea4c8e5c8" />


'experience_level' Hedef Sütununun Korelasyon Grafiği

