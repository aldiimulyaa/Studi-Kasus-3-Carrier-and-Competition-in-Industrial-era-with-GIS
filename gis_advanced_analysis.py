import math
import json
from datetime import datetime

print("==================================================================")
print(" ADVANCED GIS SPATIAL ANALYSIS & URBAN ASSET MANAGEMENT SYSTEM")
print(" Mata Kuliah: Informatics Practitioner Lecture Series 2026")
print(" Penyusun   : Aldi Mulya Fajar (G1A025091 - S1 Informatika)")
print("==================================================================\n")

# 1. Dataset Komprehensif Aset Fasilitas Publik (Koordinat Kota Bengkulu)
facilities = [
    {'id': 'AST-001', 'name': 'Puskesmas Pusat', 'type': 'Kesehatan', 'lat': -3.7928, 'lng': 102.2608, 'capacity': 500, 'operational_status': 'Aktif'},
    {'id': 'AST-002', 'name': 'Puskesmas Barat', 'type': 'Kesehatan', 'lat': -3.7980, 'lng': 102.2500, 'capacity': 300, 'operational_status': 'Aktif'},
    {'id': 'AST-003', 'name': 'Pos Pemadam Utama', 'type': 'Darurat', 'lat': -3.7850, 'lng': 102.2750, 'capacity': 450, 'operational_status': 'Aktif'},
    {'id': 'AST-004', 'name': 'Halte Transit Kota', 'type': 'Transportasi', 'lat': -3.7900, 'lng': 102.2650, 'capacity': 1200, 'operational_status': 'Renovasi'}
]

# 2. Fungsi Rumus Haversine untuk Perhitungan Jarak Geodesik Riil (dalam meter)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius rata-rata bumi dalam meter
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# 3. Fungsi Simulasi Pembuatan Poligon Lingkaran Buffer Sederhana (GeoJSON Geometry)
def create_approximate_buffer_polygon(lat, lng, radius_meters, num_points=16):
    """
    Menghasilkan list koordinat [lng, lat] berbentuk lingkaran aproksimasi 
    sebagai bentuk poligon buffer spasial standar GeoJSON.
    """
    coordinates = []
    # 1 derajat garis lintang (latitude) ~= 111,000 meter
    lat_deg_per_meter = 1.0 / 111000.0
    # 1 derajat garis bujur (longitude) menyesuaikan dengan cosinus garis lintang
    lng_deg_per_meter = 1.0 / (111000.0 * math.cos(math.radians(lat)))

    for i in range(num_points + 1):
        angle = 2 * math.pi * i / num_points
        dx = radius_meters * math.cos(angle)
        dy = radius_meters * math.sin(angle)
        
        p_lat = lat + (dy * lat_deg_per_meter)
        p_lng = lng + (dx * lng_deg_per_meter)
        coordinates.append([p_lng, p_lat])
        
    return coordinates

print(f"[INFO] Memuat {len(facilities)} data inventaris aset spasial kota...")
for f in facilities:
    print(f" - [{f['id']}] {f['name']} ({f['type']}) | Status: {f['operational_status']} | Koordinat: ({f['lat']}, {f['lng']})")
print("-" * 66 + "\n")

# 4. Eksekusi Analisis Spasial Buffer & Evaluasi Kapasitas
buffer_radius_meters = 1000.0  # Standar Radius Jangkauan Layanan 1 KM
analysis_results = []
geojson_features = []

print(f"[INFO] Menjalankan Analisis Spasial Buffer (Radius: {buffer_radius_meters} Meter)...\n")

for f in facilities:
    service_area_ha = (math.pi * (buffer_radius_meters ** 2)) / 10000.0
    
    # Evaluasi beban / kategori jangkauan layanan kota
    coverage_status = "Optimal" if f['operational_status'] == 'Aktif' else "Terbatas/Evaluasi"

    # Menyimpan hasil ringkasan terstruktur
    result_item = {
        "asset_id": f['id'],
        "name": f['name'],
        "type": f['type'],
        "coordinate": {"lat": f['lat'], "lng": f['lng']},
        "buffer_radius_m": buffer_radius_meters,
        "service_area_hectares": round(service_area_ha, 2),
        "coverage_status": coverage_status
    }
    analysis_results.append(result_item)

    print(f"Hasil Analisis Aset [{f['id']} - {f['name']}]:")
    print(f"  - Kategori Tipe       : {f['type']}")
    print(f"  - Kapasitas Pelayanan : {f['capacity']} orang/hari")
    print(f"  - Luas Area Jangkauan : {service_area_ha:.2f} Hektar")
    print(f"  - Status Cakupan GIS  : {coverage_status}")
    print("-" * 66)

    # Membuat Feature Titik (Point Feature) untuk GeoJSON
    point_feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [f['lng'], f['lat']]
        },
        "properties": {
            "id": f['id'],
            "name": f['name'],
            "category": f['type'],
            "feature_type": "Asset Location"
        }
    }
    geojson_features.append(point_feature)

    # Membuat Feature Poligon Buffer (Polygon Feature) untuk GeoJSON
    polygon_coords = create_approximate_buffer_polygon(f['lat'], f['lng'], buffer_radius_meters)
    buffer_polygon_feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [polygon_coords]
        },
        "properties": {
            "id": f['id'] + "-BUF",
            "name": f['name'] + " Buffer Zone",
            "radius_meters": buffer_radius_meters,
            "feature_type": "Spatial Buffer"
        }
    }
    geojson_features.append(buffer_polygon_feature)

# 5. Analisis Matriks Jarak Antar Aset (Spatial Distance Matrix)
print("\n[INFO] Menghitung Matriks Jarak Antar Fasilitas (Spatial Distance Matrix):")
for i in range(len(facilities)):
    for j in range(i + 1, len(facilities)):
        loc1 = facilities[i]
        loc2 = facilities[j]
        dist = haversine_distance(loc1['lat'], loc1['lng'], loc2['lat'], loc2['lng'])
        print(f"  * Jarak [{loc1['id']}] {loc1['name']} <---> [{loc2['id']}] {loc2['name']}: {dist:.2f} meter")

# 6. Menyusun Format Dokumen Ekspor GeoJSON Lengkap
master_geojson = {
    "type": "FeatureCollection",
    "metadata": {
        "project_title": "Urban Asset GIS & Spatial Buffer Analysis",
        "author": "Aldi Mulya Fajar",
        "npm": "G1A025091",
        "study_program": "S1 Informatika - Universitas Bengkulu",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    "features": geojson_features
}

print("\n==================================================================")
print(" DOKUMEN HASIL EKSPOR FORMAT GEOJSON (STANDAR SIG / WEB GIS)")
print("==================================================================")
# Menampilkan cuplikan ringkas struktur GeoJSON agar tidak terlalu panjang di terminal
print(json.dumps({
    "type": master_geojson["type"],
    "metadata": master_geojson["metadata"],
    "total_features_generated": len(master_geojson["features"])
}, indent=2))
print("==================================================================\n")
print("[SUCCESS] Seluruh modul analisis geospasial lanjutan berhasil dieksekusi!")