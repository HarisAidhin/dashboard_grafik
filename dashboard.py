"""
Tugas Visualisasi Data - Dashboard Streamlit
Studi Kasus 1, 2, dan 3 (Tipe Data & Pemilihan Visualisasi)

Nama : Haris Aidhin Ramadhan
NIM  : 241051022

Jalankan dengan:
    pip install streamlit pandas numpy plotly
    streamlit run dashboard_visdat.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

NAMA = "Haris Aidhin Ramadhan"
NIM = "241051022"

st.set_page_config(page_title="Dashboard Visualisasi Data", page_icon="📊", layout="wide")


# ---------------------------------------------------------------- DATA
@st.cache_data
def data_kasus1() -> pd.DataFrame:
    """Dataset Operasional Penjualan (2 baris pertama sesuai soal)."""
    rng = np.random.default_rng(241051022)
    produk = {
        "Laptop": ("Elektronik", 8_500_000),
        "Smartphone": ("Elektronik", 4_200_000),
        "Headphone": ("Elektronik", 650_000),
        "Buku": ("Pendidikan", 75_000),
        "Alat Tulis": ("Pendidikan", 25_000),
        "Kursus Online": ("Pendidikan", 350_000),
        "Kemeja": ("Fashion", 180_000),
        "Sepatu": ("Fashion", 450_000),
    }
    rows = [
        ("Laptop", "Elektronik", 8_500_000, 45, pd.Timestamp("2024-01-01")),
        ("Buku", "Pendidikan", 75_000, 120, pd.Timestamp("2024-01-02")),
    ]
    tanggal = pd.date_range("2024-01-03", periods=58, freq="D")
    for t in tanggal:
        nama = rng.choice(list(produk))
        kat, harga = produk[nama]
        harga = int(harga * rng.uniform(0.9, 1.1) // 1000 * 1000)
        jumlah = int(rng.integers(5, 150))
        rows.append((nama, kat, harga, jumlah, t))
    return pd.DataFrame(rows, columns=["Produk", "Kategori", "Harga (Rp)", "Jumlah Terjual", "Tanggal"])


@st.cache_data
def data_kasus2() -> pd.DataFrame:
    """Dataset Profil Mahasiswa (2 baris pertama sesuai soal)."""
    rng = np.random.default_rng(241051022)
    jurusan = ["Sistem Informasi", "Manajemen", "Informatika", "Akuntansi", "Teknik Industri"]
    rows = [("Sistem Informasi", 3, 3.85, 20), ("Manajemen", 1, 3.50, 19)]
    for _ in range(98):
        sem = int(rng.integers(1, 9))
        ipk = round(float(np.clip(rng.normal(3.3, 0.35), 2.0, 4.0)), 2)
        usia = int(np.clip(round(17.5 + sem / 2 + rng.normal(0, 0.8)), 17, 30))
        rows.append((rng.choice(jurusan), sem, ipk, usia))
    # beberapa outlier agar box plot lebih menarik
    rows += [("Informatika", 6, 2.05, 21), ("Akuntansi", 4, 3.98, 29)]
    df = pd.DataFrame(rows, columns=["Jurusan", "Semester", "IPK", "Usia"])
    df["Semester"] = pd.Categorical(df["Semester"], categories=range(1, 9), ordered=True)
    return df


@st.cache_data
def data_kasus3() -> pd.DataFrame:
    """Dataset Pengamatan Cuaca (2 baris pertama sesuai soal)."""
    rng = np.random.default_rng(241051022)
    kota = {
        "Jakarta": 32, "Bandung": 25, "Surabaya": 33, "Medan": 31,
        "Yogyakarta": 29, "Makassar": 32, "Denpasar": 30, "Semarang": 31,
    }
    rows = [("Jakarta", 32.5, 75, "Cerah"), ("Bandung", 24.0, 85, "Hujan")]
    for _ in range(78):
        k = rng.choice(list(kota))
        suhu = round(float(rng.normal(kota[k], 2)), 1)
        # suhu rendah -> cenderung lembap & hujan
        lembap = int(np.clip(rng.normal(100 - (suhu - 20) * 2.2, 8), 30, 100))
        if lembap > 82:
            kondisi = rng.choice(["Hujan", "Berawan"], p=[0.7, 0.3])
        elif lembap > 68:
            kondisi = rng.choice(["Berawan", "Cerah", "Hujan"], p=[0.5, 0.3, 0.2])
        else:
            kondisi = rng.choice(["Cerah", "Berawan"], p=[0.8, 0.2])
        rows.append((k, suhu, lembap, kondisi))
    return pd.DataFrame(rows, columns=["Kota", "Suhu (°C)", "Kelembaban (%)", "Kondisi"])


# ---------------------------------------------------------------- HELPER
def tabel_tipe(rows):
    st.subheader("Klasifikasi Tipe Data")
    st.dataframe(
        pd.DataFrame(rows, columns=["Kolom", "Tipe Data", "Skala", "Visualisasi yang Cocok"]),
        use_container_width=True, hide_index=True,
    )


def header(judul: str, deskripsi: str):
    st.title(judul)
    st.caption(f"👤 **{NAMA}**  |  🎓 **NIM {NIM}**")
    st.write(deskripsi)
    st.divider()


# ---------------------------------------------------------------- KASUS 1
def kasus1():
    header("Studi Kasus 1: Dataset Operasional Penjualan",
           "Data penjualan dengan kolom kategorik, numerik (diskrit & kontinu), dan waktu.")
    df = data_kasus1()

    st.subheader("Data")
    st.dataframe(df, use_container_width=True, hide_index=True)

    tabel_tipe([
        ("Produk", "Kategorik", "Nominal", "Bar Chart / Pie Chart"),
        ("Kategori", "Kategorik", "Nominal", "Bar Chart / Pie Chart"),
        ("Harga (Rp)", "Numerik (Kontinu)", "Rasio (punya nol absolut)", "Histogram"),
        ("Jumlah Terjual", "Numerik (Diskrit)", "Rasio (hasil hitung bulat)", "Histogram / Bar"),
        ("Tanggal", "Waktu", "Interval", "Line Chart (tren waktu)"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Kategorik (Nominal) – Bar Chart: Produk")
        d = df["Produk"].value_counts().reset_index()
        d.columns = ["Produk", "Jumlah Transaksi"]
        st.plotly_chart(px.bar(d, x="Produk", y="Jumlah Transaksi", color="Produk"), use_container_width=True)
    with c2:
        st.subheader("Kategorik (Nominal) – Pie Chart: Kategori")
        d = df.groupby("Kategori", as_index=False)["Jumlah Terjual"].sum()
        st.plotly_chart(px.pie(d, names="Kategori", values="Jumlah Terjual"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Numerik Kontinu (Rasio) – Histogram: Harga")
        st.plotly_chart(px.histogram(df, x="Harga (Rp)", nbins=15), use_container_width=True)
    with c4:
        st.subheader("Numerik Diskrit (Rasio) – Histogram: Jumlah Terjual")
        st.plotly_chart(px.histogram(df, x="Jumlah Terjual", nbins=15), use_container_width=True)

    st.subheader("Waktu (Interval) – Line Chart: Tren Jumlah Terjual")
    d = df.groupby("Tanggal", as_index=False)["Jumlah Terjual"].sum()
    st.plotly_chart(px.line(d, x="Tanggal", y="Jumlah Terjual", markers=True), use_container_width=True)


# ---------------------------------------------------------------- KASUS 2
def kasus2():
    header("Studi Kasus 2: Dataset Profil Mahasiswa",
           "Data profil mahasiswa dengan kategorik nominal, kategorik ordinal, dan numerik kontinu.")
    df = data_kasus2()

    st.subheader("Data")
    st.dataframe(df, use_container_width=True, hide_index=True)

    tabel_tipe([
        ("Jurusan", "Kategorik", "Nominal (hanya label pembeda)", "Bar Chart / Pie Chart"),
        ("Semester", "Kategorik", "Ordinal (ada tingkatan 1 → 2 → 3)", "Bar Chart Berurutan"),
        ("IPK", "Numerik (Kontinu)", "Rentang / desimal", "Histogram, Box Plot"),
        ("Usia", "Numerik (Kontinu)", "Rentang / desimal", "Histogram, Box Plot"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Nominal – Bar Chart: Jurusan")
        d = df["Jurusan"].value_counts().reset_index()
        d.columns = ["Jurusan", "Jumlah Mahasiswa"]
        st.plotly_chart(px.bar(d, x="Jurusan", y="Jumlah Mahasiswa", color="Jurusan"), use_container_width=True)
    with c2:
        st.subheader("Ordinal – Bar Chart Berurutan: Semester")
        d = df["Semester"].value_counts().sort_index().reset_index()
        d.columns = ["Semester", "Jumlah Mahasiswa"]
        d["Semester"] = d["Semester"].astype(str)
        fig = px.bar(d, x="Semester", y="Jumlah Mahasiswa")
        fig.update_xaxes(categoryorder="array", categoryarray=[str(i) for i in range(1, 9)])
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Kontinu – Histogram: IPK (distribusi)")
        st.plotly_chart(px.histogram(df, x="IPK", nbins=15), use_container_width=True)
    with c4:
        st.subheader("Kontinu – Histogram: Usia (distribusi)")
        st.plotly_chart(px.histogram(df, x="Usia", nbins=12), use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        st.subheader("Kontinu – Box Plot: IPK (sebaran & outlier)")
        st.plotly_chart(px.box(df, y="IPK", points="outliers"), use_container_width=True)
    with c6:
        st.subheader("Kontinu – Box Plot: Usia (sebaran & outlier)")
        st.plotly_chart(px.box(df, y="Usia", points="outliers"), use_container_width=True)


# ---------------------------------------------------------------- KASUS 3
def kasus3():
    header("Studi Kasus 3: Dataset Pengamatan Cuaca",
           "Data cuaca dengan kategorik nominal, numerik interval (suhu), dan numerik rasio (kelembaban).")
    df = data_kasus3()

    st.subheader("Data")
    st.dataframe(df, use_container_width=True, hide_index=True)

    tabel_tipe([
        ("Kota", "Kategorik", "Nominal (label teks tanpa urutan)", "Bar Chart"),
        ("Suhu (°C)", "Numerik", "Interval (0°C bukan 'tidak ada suhu')", "Histogram, Box Plot"),
        ("Kelembaban (%)", "Numerik", "Rasio (0% = benar-benar tidak ada kelembaban)", "Histogram, Box Plot"),
        ("Kondisi", "Kategorik", "Nominal (label teks tanpa urutan)", "Bar Chart / Pie Chart"),
    ])

    st.info(
        "**Interval vs Rasio:** pada skala interval (suhu °C) jarak antar nilai sama, tetapi 0°C bukan "
        "titik nol absolut, sehingga 20°C **bukan** 2× lebih panas dari 10°C. Pada skala rasio "
        "(kelembaban %) 0% berarti benar-benar tidak ada kelembaban, sehingga perbandingan rasio berlaku."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Nominal – Bar Chart: Rata-rata Suhu per Kota")
        d = df.groupby("Kota", as_index=False)["Suhu (°C)"].mean().round(1)
        st.plotly_chart(px.bar(d, x="Kota", y="Suhu (°C)", color="Kota", text="Suhu (°C)"), use_container_width=True)
    with c2:
        st.subheader("Nominal – Pie Chart: Kondisi Cuaca")
        d = df["Kondisi"].value_counts().reset_index()
        d.columns = ["Kondisi", "Jumlah"]
        st.plotly_chart(px.pie(d, names="Kondisi", values="Jumlah"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Interval – Histogram: Suhu (°C)")
        st.plotly_chart(px.histogram(df, x="Suhu (°C)", nbins=15), use_container_width=True)
    with c4:
        st.subheader("Rasio – Histogram: Kelembaban (%)")
        st.plotly_chart(px.histogram(df, x="Kelembaban (%)", nbins=15), use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        st.subheader("Box Plot: Suhu (°C) per Kondisi")
        st.plotly_chart(px.box(df, x="Kondisi", y="Suhu (°C)", color="Kondisi"), use_container_width=True)
    with c6:
        st.subheader("Scatter: Suhu vs Kelembaban")
        st.plotly_chart(px.scatter(df, x="Suhu (°C)", y="Kelembaban (%)", color="Kondisi", hover_data=["Kota"]),
                        use_container_width=True)


# ---------------------------------------------------------------- MAIN
st.sidebar.title("📊 Visualisasi Data")
st.sidebar.markdown(f"**Nama:** {NAMA}  \n**NIM:** {NIM}")
st.sidebar.divider()
pilihan = st.sidebar.radio(
    "Pilih Studi Kasus",
    ["Kasus 1: Operasional Penjualan", "Kasus 2: Profil Mahasiswa", "Kasus 3: Pengamatan Cuaca"],
)

if pilihan.startswith("Kasus 1"):
    kasus1()
elif pilihan.startswith("Kasus 2"):
    kasus2()
else:
    kasus3()

st.divider()
st.caption(f"Dibuat oleh {NAMA} (NIM {NIM}) – Tugas Mata Kuliah Visualisasi Data")