# Period Tracker 🩸🩸🩸

Period Tracker adalah sebuah aplikasi yang, sesuai namanya, berfungsi untuk membantu wanita untuk merekam jejak siklus menstruasi yang dialaminya beserta gejala yang dapat terjadi pada siklus tersebut. Selain itu, terdapat fungsi-fungsi tambahan seperti prediksi siklus menstruasi dan artikel-artikel seputar menstruasi yang turut membantu wanita menghadapi fenomena yang terjadi sekali sebulan tersebut.

## Feature Set

- [x] Menampilkan kalender 📆
- [x] Menerima masukan kapan siklus menstruasi terjadi ✍️
- [x] Menerima masukan gejala menstruasi dari pengguna dengan opsi untuk membuat gejala baru 🤕
- [x] Menampilkan informasi riwayat siklus menstruasi serta gejalanya 🤢
- [x] Membuat prediksi kapan waktu siklus menstruasi selanjutnya dalam sebuah _user-defined range_ 🔮
- [x] Memberikan _reminder_ dan _alarm_ untuk prediksi siklus menstruasi berikutnya pada _user-defined time_ ⏰
- [x] Menampilkan artikel-artikel tentang menstruasi dan kesehatan reproduksi 📆

## Dependencies

`Python 3.10`  
`PyQt5`

## Modul

#### App

Dhanika N.

#### Article

Brigita T. C. & Fatih N. R. I.

#### Article Page

Brigita T. C. & Fatih N. R. I.

#### ChangeMenstrualStatus

Dhanika N. & Fatih N. R. I.

#### Database

Fatih N. R. I.

#### Kalendar

Dhanika N., Althaaf K. A., & Fatih N. R. I.

#### Notification

Brigita T. C.

#### Alarm Clock

Brigita T. C.

#### PredictionManager

Althaaf K. A. & Fatih N. R. I.

#### Settings

Brigita T. C. & Fatih N. R. I.

#### Symptom Forms

Puti N. A. & Fatih N. R. I.

## How to Use

1. Pastikan seluruh _dependencies_ yang ada di [di sini](#dependencies) telah dipasang pada komputer dengan OS Windows(aplikasi hanya berjalan pada Windows)
2. _Download_ atau _clone_ kode dari aplikasi di _repository_ ini ke komputer tempat aplikasi ingin digunakan.
3. Jalankan _file_ `src/App.py`
4. _Start tracking your period!_

## Database Tables

1. MenstrualCycle

- IdCycle
- StartDate
- Duration

2. MenstrualSymptoms

- Date
- Name
- BuiltIn
- Desc
- Rate

3. MenstrualPrediction

- IdPrediction
- Start_Date
- Duration

4. UserSetting

- PredictionRange
- ReminderTime

5. Articles

- IdArticle
- Title
- Summary
- Content
