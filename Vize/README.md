# Makine Öğrenmesi ile Çalışan Deneyim Seviyesi Sınıflandırması
Bu proje makine öğrenmesi kullanarak belirli meslek gruplarındaki çalışanların verilerini kullanarak maaş ve deneyim seviyesi tahmini yapılmaya çalışılmaktadır. Regresyon ile maaş tahmini ve Random Forest ile deneyim seviyesi tahmini olarak iki farklı yaklaşım denenmiş ve verisetinin bu yaklaşımlara uygunluğu karşılaştırılmıştır.

# 1. Veri Setinin Eğitime Hazırlanması
Maaş tahmini için: 'work_year', 'experience_level', 'employment_type', 'job_title','remote_ratio', 'company_location', 'company_size' sütunları kullanılırken, deneyim seviyesi tahmini için ise 'work_year', 'employment_type', 'job_title','salary_in_usd','remote_ratio', 'company_location', 'company_size' sütunları kullanılmıştır.

### Verinin filtrelenmesi
Veride bulunan 'job_title' sütununda çok fazla sayıda az sayıda bulunan değer olduğu tespit edilmiş, öğrenememeye yol açmaması için önce bu satırların çıkarılmaları denenmiş ancak bunun da veri setinin büyük kısmının atılmasına, bunun sonucu olarak da zaten az değer bulunan bazı değerler için('experience_level' sütununun EN ve EX değerleri) öğrenememeye yol açtığı görülmüş ve bu doğrultuda other_EN, other_EX, other_MI ve other_SE olarak yeni iş unvanı değerleri altında gruplandırılmıştır. Bu işlemin modelin deneyim tahmini başarısını %5 civarı bir oranda arttırdığı, özellikle de EN ve EX değerleri sütunlarda pozitif bir etki yaptığı görülmüştür.

### Kategorik Dönüşüm
Ordinal Encoding: Sıralı veri içeren experience_level (EN < MI < SE < EX) ve company_size (S < M < L) sütunları sıralı olarak sayısal değerlere dönüştürülmüştür.

One-Hot Encoding: Sıralı olmayan job_title, employment_type gibi nominal veriler 0 ve 1 değerlerine çevrilmiştir.

### Eğitim ve Test verilerinin ayırma
Bu işlemler sonucunda eğitime hazır hale getirilen verisetinin %80'i eğitim %20'si de test için ayırılmıştır.

# 2. Maaş Tahmin Modeli
Filtrelenmiş ve kategorik dönüşümleri yapılmış veri üzerinde Random Forest, Linear Regression, Decision Tree ve Gradient Boosting yöntemleri denenmiş ve şu sonuçlar alınmıştır:
<img width="515" height="66" alt="Screenshot 2025-12-06 at 21 28 22" src="https://github.com/user-attachments/assets/9db2345c-9713-4a6f-9c10-16775331d21f" />
Görselde de görüldüğü gibi denenen metodların başarı oranları birbirine yakın olsa da az farkla Gradient Boosting yöntemi daha başarılı sonuç vermiştir. Veri üzerinde yapılan işlemlere rağmen modelin başarı düzeyi beklenenin altında kalmıştır ve bu verilerin maaş(salary_in_usd) tahmini yapmaya uygun olmadığı sonucuna varılmıştır.

# 3. Deneyim Seviyesi Tahmin Modeli
Maaş tahmininde istenilen sonucun elde edilememesi üzerine deneyim(experience_level) tahminine yönenilmiş ve Random Forest, Logistic Regression, Decision Tree ve Gradient Boosting yöntemleri kullanılarak yapılan eğitim ve tahmin testleri sonucunda görseldeki başarı oranları elde edilmiştir. En başarılı yöntem Random Forest yaklaşımı olmuştur
<img width="401" height="79" alt="Screenshot 2025-12-06 at 21 34 54" src="https://github.com/user-attachments/assets/25d2c9ec-a5c4-42ee-a048-154d86c03e0d" />

# 4. Sonuç ve Çıkarımlar
Yapılan işlemler sonucunda eldeki verisetinin sayısal değerlerden oluşan 'salary_in_usd' sütunundansa kategorik değerler içeren 'experience_level' sütununu tahmin etmeye daha elverişli olduğu görülmüştür. Regresyon ile maaş tahmin modeli düşük bir R skoru elde edip maaşın değerini verideki değer sütunlarla açıklamada yetersiz kalırken, deneyim seviyesi tahmini için Random Forest algoritması ile oluşturulan model %78 gibi bir doğruluk oranı elde edip çok daha başarılı olmuştur.
Aradaki bu büyük farkın temel nedeni maaşın, elimizdeki veride bulunmayan bir çok dış etkene de bağlı olmasıdır. Deneyim düzeyi ise en aşağıda eklenen tabloya da bakacak olursak maaş ile doğrudan orantılıdır ve yüksek korelasyon gösterir. Bu nedenle maaşın hedef değil de bir feature olarak kullanıldığı bir model çok daha tutarlı sonuçlar vermiştir.
### Algoritmaların Karşılaştırmaları
Algoritmalar arasında yapılan karşılaştırmada hem regresyon hem de sınıflandırma görevlerinde ağaç tabanlı modellerin (Random Forest ve Gradient Boosting) doğrusal modellere (Linear ve Logistic Regression) kıyasla daha yüksek performans verdiği gözlemlenmiştir. Bu durum, veri setindeki özellikler ile hedef değişkenler arasındaki ilişkinin doğrusal olmaktan ziyade daha karmaşık ve hiyerarşik bir yapıda olduğunu kanıtlamaktadır. Dolayısıyla bu tip veri setlerinde karmaşık ilişkileri modelleyebilen algoritmaların tercih edilmesi gerekmektedir.
### Veri Dengesizliğinin Sonuca Etkisi
Modelin sonucundan oluşturulan hit/miss grafiğinden de görülebileceği gibi veri dengesizliğinden dolayı model, az sayıda bulunan 'EX' ve 'EN' değerlerini tahmin ederken düşük başarı göstermiş, en yüksek sayıda verinin bulunduğu 'SE' değerini tahmin ederken ise en yüksek başarı oranını göstermiştir.
### Genel Değerlendirme
Oluşturulan modeller sonucunda başarılı bir maaş tahmini yapılamazken, başarılı sayılabilecek vir deneyim seviyesi tahmini yapılabilmektedir. Eldeki gürültülü veri ile, uygulanan filtreleme ve gruplandırma işlemlerinin de yardımı ile %78 gibi bir oranla tahmin yapan bir model eğitilmiş verinin yapısal özelliklerinin regresyon yerine sınıflandırma problemlerine daha uygun olduğu ortaya konmuştur.

<img width="773" height="443" alt="Screenshot 2025-11-25 at 09 44 11" src="https://github.com/user-attachments/assets/57660de1-efc4-4709-977d-ca8fda49844c" />

<img width="642" height="515" alt="Screenshot 2025-11-25 at 09 44 05" src="https://github.com/user-attachments/assets/ff983cc3-5546-4c5e-b330-4aca5d7ad591" />

<img width="752" height="461" alt="Screenshot 2025-11-25 at 09 43 46" src="https://github.com/user-attachments/assets/0fa6bef9-d908-4b08-a5da-3dbbe7fa4462" />

