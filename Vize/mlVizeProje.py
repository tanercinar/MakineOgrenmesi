import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression, Ridge, SGDRegressor, PassiveAggressiveRegressor, BayesianRidge
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, 
                            BaggingRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor)
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import LinearSVR

#Veriyi değişkene atama
data = pd.read_csv('Dataset salary 2024.csv')
data.dropna(inplace=True)
print(data.head())
#Veride gürültünün fazla olduğu 'job_title' sütununu filtreleyip
#nadir olanların hepsini tek bir 'Other' çatısı altında topluyoruz.
valid_percentage = len(data) * 0.002 # %1 eşik değeri
job_counts = data['job_title'].value_counts()

#Eşiğin altında kalan nadir unvanlar
rare_jobs = job_counts[job_counts < valid_percentage].index

#Nadir unvanları 'Other' olarak değiştir
data.loc[data['job_title'].isin(rare_jobs), 'job_title'] = 'Other'

#Filtrelenmiş veriyi yeni bir dataframe'e kopyalama
data_filtered = data.copy()

#Kontrol için sonucu ekrana yazdırma
print(f"Orijinal Veri Sayısı: {len(data)}")
print(f"İşlem Sonrası Benzersiz İş Unvanı Sayısı: {data_filtered['job_title'].nunique()}")
print("-" * 30)

#Filtrelenmiş verideki target ve feature sütunlarını ayarlama
target = 'salary_in_usd'
features = ['experience_level', 'work_year', 'employment_type', 'job_title', 'remote_ratio', 'company_size', 'company_location']

#Sütunları X ve Y değerlerine atama
X = data_filtered[features]
y = data_filtered[target]

#Sıralı ifadeler
ordinal_cols = ['experience_level', 'company_size']
ordinal_cats = [
    ['EN', 'MI', 'SE', 'EX'], 
    ['S', 'M', 'L']
]

#Nominal ifadeler
nominal_cols = ['employment_type', 'job_title', 'company_location', 'remote_ratio', 'work_year']

#Ön işleme ile veriyi hazırlama
preprocessor = ColumnTransformer(
    transformers=[
        ('ord', OrdinalEncoder(categories=ordinal_cats), ordinal_cols),
        ('nom', OneHotEncoder(handle_unknown='ignore'), nominal_cols)
    ],
    remainder='passthrough'
)

#Veriyi böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Sınıflandırma tablosundaki modellerin Regresyon karşılıkları
models = [
    ("Linear Regression", LinearRegression()),
    ("Ridge Regressor", Ridge(random_state=42)),
    ("SGD Regressor", SGDRegressor(random_state=42)),
    ("Passive Aggressive", PassiveAggressiveRegressor(random_state=42)),
    ("K-Neighbors (KNN)", KNeighborsRegressor(n_neighbors=5)),
    ("Decision Tree", DecisionTreeRegressor(random_state=42)),
    ("Extra Tree", ExtraTreeRegressor(random_state=42)),
    ("Random Forest", RandomForestRegressor(random_state=42)),
    ("Gradient Boosting", GradientBoostingRegressor(random_state=42)),
    ("AdaBoost", AdaBoostRegressor(random_state=42)),
    ("Bagging Regressor", BaggingRegressor(random_state=42)),
    ("Extra Trees", ExtraTreesRegressor(random_state=42)),
]

best_model = None
best_score = -float('inf')
best_name = ""

print(f"Toplam {len(models)} farklı model test edilecek...")
print("-" * 60)

#Döngüyle matris içindeki modelleri pipeline ile birleştirerek başarı oranlarına bak
for name, model in models:
    try:
        #Modeli pipeline içinde hazırla
        model_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', model)
        ])
        
        #Modeli eğit
        model_pipeline.fit(X_train, y_train)
        y_pred = model_pipeline.predict(X_test)
        
        #Modelin başarısını hesapla
        score = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"{name:25} -> R2 Score: {score:.4f} | MAE: ${mae:,.0f}")
        
        if score > best_score:
            best_score = score
            best_model = model_pipeline
            best_name = name
    except Exception as e:
        print(f"{name:25} -> HATA: {e}")

print("-" * 60)
print(f"EN İYİ MODEL: {best_name} (R2: {best_score:.4f})")
print("-" * 60)

#Sonuçları görselleştirme (Sadece en iyi model için)

#En iyi model ile tahmin alma
y_pred_best = best_model.predict(X_test)

#Gerçek ve tahmin edilen değerleri grafiğe dökme
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred_best, alpha=0.5, color='blue', label='Tahminler')

#İdeal tahmin çizgisini ekleme
min_val = min(y_test.min(), y_pred_best.min())
max_val = max(y_test.max(), y_pred_best.max())
plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', linewidth=2, label='İdeal Tahmin Çizgisi')

plt.title(f'{best_name} - Gerçek Maaş vs Tahmin Edilen Maaş')
plt.xlabel('Gerçek Maaş (USD)')
plt.ylabel('Tahmin Edilen Maaş (USD)')
plt.legend()
plt.grid(True)
plt.show()

#Hata dağılımını çizdirme
residuals = y_test - y_pred_best
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, color='purple')
plt.title(f'{best_name} - Hata Miktarı Dağılımı (Residuals)')
plt.xlabel('Hata (Gerçek - Tahmin)')
plt.ylabel('Frekans')
plt.axvline(0, color='red', linestyle='--')
plt.show()
