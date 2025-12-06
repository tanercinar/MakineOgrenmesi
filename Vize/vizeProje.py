import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

def main():
    # 1. VERİ YÜKLEME
    # Filtreleme yapılmadan ham veriyi kullanıyoruz.
    try:
        data = pd.read_csv('Dataset salary 2024.csv')
    except FileNotFoundError:
        print("Hata: 'Dataset salary 2024.csv' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return

    data.dropna(inplace=True)
    
    print(f"İşleme alınan toplam veri sayısı: {len(data)}")
    print("Not: İş unvanı (job_title) filtrelemesi/gruplaması yapılmamıştır.")
    print("-" * 30)

    # 2. ÖZELLİKLERİN VE HEDEF DEĞİŞKENİN BELİRLENMESİ
    target = 'experience_level'
    features = ['salary_in_usd', 'work_year', 'employment_type', 'job_title', 'remote_ratio', 'company_size', 'company_location']

    X = data[features]
    y = data[target]

    # 3. ÖN İŞLEME (PREPROCESSING)
    # Sıralı ifadeler
    ordinal_cols = ['company_size']
    ordinal_vals = [['S', 'M', 'L']]

    # Nominal ifadeler
    # Filtreleme yapmadığımız için job_title'da çok fazla kategori olabilir, 
    # bu yüzden handle_unknown='ignore' önemlidir.
    nominal_cols = ['employment_type', 'job_title', 'company_location', 'remote_ratio', 'work_year']

    preprocessor = ColumnTransformer(
        transformers=[
            ('ord', OrdinalEncoder(categories=ordinal_vals), ordinal_cols),
            ('nom', OneHotEncoder(handle_unknown='ignore'), nominal_cols)
        ],
        remainder='passthrough'
    )

    # 4. EĞİTİM VE TEST SETİNE AYIRMA
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. MODEL EĞİTİMİ (RANDOM FOREST)
    print("Random Forest modeli eğitiliyor...")
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    model_pipeline.fit(X_train, y_train)
    
    # Başarı skorunu yazdır
    accuracy = model_pipeline.score(X_test, y_test)
    print(f"Random Forest için doğruluk (Accuracy): {accuracy:.5f}")
    print("-" * 30)

    # 6. GÖRSELLEŞTİRME

    # Grafik 1: Confusion Matrix (Karmaşıklık Matrisi)
    print("Grafikler oluşturuluyor...")
    plt.figure(figsize=(10, 8))
    ConfusionMatrixDisplay.from_estimator(model_pipeline, X_test, y_test)
    plt.title('Confusion Matrix (Filtresiz Veri)')
    plt.show()

    # Grafik 2: Hit/Miss Bar Grafiği
    # Tahminleri al
    y_pred = model_pipeline.predict(X_test)
    comparison_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

    # Hit ve Miss sütunlarını ekleme
    comparison_df['Outcome'] = comparison_df.apply(
        lambda row: 'Hit' if row['Actual'] == row['Predicted'] else 'Miss', axis=1
    )

    # Veriyi Hit/Miss olarak gruplama
    plot_data = comparison_df.groupby(['Actual', 'Outcome']).size().reset_index(name='Count')

    plt.figure(figsize=(12, 6))

    # Sütun grafiği oluştur
    sns.barplot(
        data=plot_data, 
        x='Actual', 
        y='Count', 
        hue='Outcome', 
        palette={'Hit': 'green', 'Miss': 'red'}
    )

    plt.title('Deneyim Seviyelerine Göre Doğru ve Yanlış Tahminler (Filtresiz)', fontsize=15)
    plt.xlabel('Deneyim Seviyesi (Target)', fontsize=13)
    plt.ylabel('Sayı', fontsize=13)
    plt.legend()
    plt.grid(True, axis='y')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()