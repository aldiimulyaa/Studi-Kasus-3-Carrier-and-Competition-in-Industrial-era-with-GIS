import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("==================================================================")
print(" MACHINE LEARNING WORKFLOW: STUDI KASUS PT MAJU BERSAMA")
print(" Narasumber : Dr. Taniza binti Tajuddin (UiTM Cawangan Kedah)")
print(" Penyusun   : Aldi Mulya Fajar (G1A025091 - S1 Informatika)")
print("==================================================================\n")

# 1. Tahap Data Collection & Dataset Simulasi (Data-Driven Approach)
print("[INFO] Tahap 1: Memuat dan Menyiapkan Dataset Historis...")
data = {
    'riwayat_transaksi': [12, 3, 25, 2, 18, 30, 5, 22, 8, 15],
    'rata_keterlambatan_hari': [2, 15, 1, 20, 3, 0, 14, 2, 10, 4],
    'jumlah_tagihan_juta': [1.5, 4.0, 2.0, 5.5, 1.2, 0.8, 3.5, 2.2, 4.5, 1.8],
    'status_terlambat': [0, 1, 0, 1, 0, 0, 1, 0, 1, 0] # 0 = Tepat Waktu, 1 = Terlambat
}

df = pd.DataFrame(data)
print(df.head(5))
print("-" * 66 + "\n")

# 2. Tahap Data Preprocessing & Pemisahan Fitur/Target
print("[INFO] Tahap 2: Data Preprocessing & Pembagian Fitur-Target...")
X = df[['riwayat_transaksi', 'rata_keterlambatan_hari', 'jumlah_tagihan_juta']]
y = df['status_terlambat']

# Membagi Data Latih (Training Data) dan Data Uji (Testing Data) - Rasio 80:20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisasi / Feature Scaling untuk menjaga kestabilan algoritma
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f" - Jumlah Data Latih (Training): {len(X_train)} baris")
print(f" - Jumlah Data Uji (Testing)  : {len(X_test)} baris")
print("-" * 66 + "\n")

# 3. Tahap Model Training (Algoritma Supervised Learning - Logistic Regression)
print("[INFO] Tahap 3: Melatih Model Algoritma Machine Learning...")
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)
print("[SUCCESS] Model berhasil dilatih menggunakan data historis perusahaan.")
print("-" * 66 + "\n")

# 4. Tahap Evaluasi Performa Model (Performance Evaluation)
print("[INFO] Tahap 4: Evaluasi Performa & Validasi Model...")
y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f" - Akurasi Model (Accuracy Score): {accuracy * 100:.2f}%")
print(" - Confusion Matrix:")
print(conf_matrix)
print("\n - Laporan Klasifikasi Lengkap (Classification Report):")
print(classification_report(y_test, y_pred, zero_division=0))
print("==================================================================")
print("[SUCCESS] Seluruh rangkaian pipeline Machine Learning selesai dieksekusi!")