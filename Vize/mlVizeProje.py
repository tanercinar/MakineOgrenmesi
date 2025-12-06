import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error

#Veriyi değişkene atama
data = pd.read_csv('Dataset salary 2024.csv')
data.dropna(inplace=True)
#Veride gürültünün fazla olduğu 'job_title' sütununu filtrleyip yeni isimlerde gruplama
valid_percentage = len(data) * 0.02
job_counts = data['job_title'].value_counts()
rare_jobs = job_counts[job_counts < valid_percentage].index

for exp_level in ['EX', 'MI', 'EN', 'SE']:
    mask = (data['job_title'].isin(rare_jobs)) & (data['experience_level'] == exp_level)
    if mask.sum() > 0:
        new_title = f"other_{exp_level}"
        data.loc[mask, 'job_title'] = new_title

job_counts = data['job_title'].value_counts()
valid_jobs = job_counts[job_counts >= valid_percentage].index
other_titles = [title for title in data['job_title'].unique() if str(title).startswith('other')]
valid_jobs = valid_jobs.union(other_titles)

#Filtrelenmiş veriyi yeni bir dataframe'e kopyalama
data_filtered = data[data['job_title'].isin(valid_jobs)].copy()

#Kontrol için sonucu ekrana yazdırma
print(f"Orijinal Veri Sayısı: {len(data)}")
print(f"Filtrelenmiş Veri Sayısı: {len(data_filtered)}")

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

#Denenecek modelleri bir matris içinde topla
models = [
    ("Random Forest", RandomForestRegressor(random_state=42)),
    ("Linear Regression", LinearRegression()),
    ("Decision Tree", DecisionTreeRegressor(random_state=42)),
    ("Gradient Boosting", GradientBoostingRegressor(random_state=42))
]

best_model = None
best_score = -float('inf')
best_name = ""


#Döngüyle matris içindeki modelleri pipeline ile birleştirerek başarı oranları arasındaki farka bak
for name, model in models:
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
    
    print(f"{name:20} -> R2 Score: {score:.4f} | Ortalama Hata (MAE): ${mae:,.0f}")
    
    if score > best_score:
        best_score = score
        best_model = model_pipeline
        best_name = name

print(f"EN İYİ MODEL: {best_name} (R2: {best_score:})")

#Sonuçları görselleştirme

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
plt.title('Hata Miktarı Dağılımı (Residuals)')
plt.xlabel('Hata (Gerçek - Tahmin)')
plt.ylabel('Frekans')
plt.axvline(0, color='red', linestyle='--')
plt.show()