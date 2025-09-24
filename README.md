# Nexlead - Promotion Employee Predictor 
Aplikasi machine learning untuk memprediksi apakah seorang karyawan masuk ke dalam kategori dipromosikan atau tidak menggunakan pengembangan model **CatBoostClassifier**. Dikembangkan juga rancangan User Interface yang dapat diakses pada link berikut <a href="https://www.canva.com/design/DAGqgnIASns/L3fdiF3fYaQhNNWL3jkPLg/view?utm_content=DAGqgnIASns&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hc3db0797f8" target="_blank">Project Nexlead</a>

---

## Latar Belakang
Banyak perusahaan yang kurang memanfaatkan data dengan optimal karena keterbatasan data berkualitas, teknologi yang tidak memadai, dan kekurangan ahli teknologi. Analisis data tidak hanya membantu mengidentifikasi calon karyawan yang berpotensi tinggi tetapi juga mengoptimalkan strategi perekrutan dan manajemen SDM. Organisasi yang memanfaatkan analisis data melaporkan peningkatan efisiensi perekrutan dan penurunan tingkat perputaran karyawan (Odionu dkk., 2024). Dengan memanfaatkan berbagai sumber data, HR dapat mengevaluasi kinerja karyawan dan potensi mereka untuk peran kepemimpinan, memastikan sistem promosi berdasarkan prestasi yang mereka miliki dan selaras dengan tujuan perusahaan (Tang dkk., 2020).

## Tujuan Projek
Tujuan dari projek ini adalah membantu HR dalam mengambil keputusan yang lebih objektif dan berdasarkan data, meningkatkan efektivitas program pengembangan dan pelatihan karyawan, serta memberikan kontribusi positif terhadap promosi karyawan.

## Dataset
Dataset yang dikumpulkan dan digunakan adalah Data Kinerja Karyawan untuk Analisis Sumber Daya Manusia yang diperoleh dari Kaggle (Sanjana Chaudari, 2023). 

## Pemilihan Algoritma
Kami menggunakan model Cat Boost Classifier karena algoritma ini dirancang untuk meminimalkan overfitting melalui pendekatan gradient boosting yang unik, yang bermanfaat dalam skenario dengan data yang terbatas (Wang et al., 2024). Cat Boost secara native mendukung fitur kategorikal, memungkinkan input langsung tanpa enkoding yang rumit, sehingga mempermudah proses pemodelan (Saxena & Maurya, 2024).

## Web Application
<img src="\screen\tampilan_2.JPG" alt="Preview" width="600"/>
Demo app: <a href="https://www.canva.com/design/DAGqgnIASns/L3fdiF3fYaQhNNWL3jkPLg/view?utm_content=DAGqgnIASns&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hc3db0797f8" target="_blank">Project Nexlead</a>

## Hasil Prediksi
- Model akan menampilkan apakah karyawan tersebut dipromosikan atau tidak.
- Diberikan rekomendasi untuk HR untuk step selanjutnya berdasarkan kinerja karyawannya
