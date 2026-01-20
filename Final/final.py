import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

#verinin yüklemesi değşkene aktarılması ve temizlenmesi
df = pd.read_csv('Smart_Bin.csv').dropna()

#ödevden istenilen pivotların oluşturulması
pivot_fl_b = pd.pivot_table(df, values='FL_B', index='Container Type', columns='Recyclable fraction', aggfunc='mean')
pivot_fl_a = pd.pivot_table(df, values='FL_A', index='Container Type', columns='Recyclable fraction', aggfunc='mean')

#konteynr bazlı genel ortalamalar
pivot_b_avg = df.groupby('Container Type')['FL_B'].mean().reset_index().rename(columns={'FL_B': 'avg_FL_B'})
pivot_a_avg = df.groupby('Container Type')['FL_A'].mean().reset_index().rename(columns={'FL_A': 'avg_FL_A'})

#pivot bilgilerini ana tabloya eklenmesi
df = df.merge(pivot_b_avg, on='Container Type', how='left')
df = df.merge(pivot_a_avg, on='Container Type', how='left')

#kategorik verilerin encoder ile sayısallaştırılması
le_container = LabelEncoder()
le_fraction = LabelEncoder()
le_class = LabelEncoder()
df['Container Type Encoded'] = le_container.fit_transform(df['Container Type'])
df['Recyclable fraction Encoded'] = le_fraction.fit_transform(df['Recyclable fraction'])
df['Class_Encoded'] = le_class.fit_transform(df['Class'])

#özellik ve hedef değişken seçilmesi
features = ['FL_B', 'FL_A', 'VS', 'FL_B_3', 'FL_A_3', 'FL_B_12', 'FL_A_12', 'Container Type Encoded', 'Recyclable fraction Encoded', 'avg_FL_B', 'avg_FL_A']
x = df[features]
y = df['Class_Encoded']

#standart scalaer iile ölçeklendirme yapılması
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

#eğitim test verilerini ayırılması
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)

#modellerin tanımlanması
models = {
    "Logistic Regression": LogisticRegression(max_iter=2000),
    "KNN Classification": KNeighborsClassifier(n_neighbors=7),
    "Random Forest": RandomForestClassifier(n_estimators=150, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=10),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
}

#modellerin eğitilmesi ve değerlendirilmesi
trained_models = {}
acc_scores = []

for isim, model in models.items():
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    trained_models[isim] = y_pred
    accuracy = accuracy_score(y_test, y_pred)
    acc_scores.append(accuracy)
    print(f"doğruluk {accuracy*100:.4f}")
    print(classification_report(y_test, y_pred, target_names=le_class.classes_))

#confusion matrix
plt.figure(figsize=(14, 7))
#en iyi sonucu veren model olduğu için tamamının çıktısında random forest kullanıyorum
cm = confusion_matrix(y_test, trained_models["Random Forest"])
sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', xticklabels=le_class.classes_, yticklabels=le_class.classes_)
plt.title('Random Forest İçin Confusion Matrix')
plt.xlabel('Tahmin Edilen Değer')
plt.ylabel('Gerçek Değer')
plt.tight_layout()
plt.savefig("plot1.png", dpi=300, bbox_inches='tight')
plt.show()

#model karşılaştırması grafiği
plt.figure(figsize=(14, 7))
model_compare_df = pd.DataFrame({'Model': list(models.keys()), 'Accuracy': acc_scores})
plt.bar(model_compare_df['Model'], model_compare_df['Accuracy'], color='darkblue')
plt.ylim(0, 1.0)
plt.title('Model Karşılaştırması')
plt.ylabel('Doğruluk Skoru (Accuracy)')
plt.xlabel('Model')
plt.xticks(rotation=18)
for i, (model, acc) in enumerate(zip(model_compare_df['Model'], model_compare_df['Accuracy'])):
    plt.text(i, acc + 0.01, f'{acc*100:.4f}%', ha='center', fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("plot2.png", dpi=300, bbox_inches='tight')
plt.show()

#feature importance grafiği
rf_model = models["Random Forest"]
fi_df = pd.DataFrame({'Feature': features, 'Importance': rf_model.feature_importances_})
fi_df = fi_df.sort_values(by='Importance', ascending=False)

plt.figure(figsize=(12, 9))
plt.barh(fi_df['Feature'], fi_df['Importance'], color='darkgreen')
plt.title('Özellik Önem Sıralaması')
plt.xlabel('Önem Skoru')
plt.ylabel('Özellikler')
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("plot3.png", dpi=300, bbox_inches='tight')
plt.show()