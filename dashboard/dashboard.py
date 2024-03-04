import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset dari file csv
data_day = pd.read_csv('day.csv')
data_hour = pd.read_csv('hour.csv')
print(data_day.head())
print(data_hour.head())

# Menampilkan informasi umum dataset
print(data_day.info())
print(data_hour.info())

# Menampilkan beberapa baris pertama dataset
print(data_day.head())
print(data_hour.head())

# Mengecek jumlah data yang unik dalam kolom 'datetime'
print(data_day['dteday'].nunique())
print(data_hour['dteday'].nunique())

# Mengecek nilai yang hilang atau null
print(data_day.isnull().sum())
print(data_hour.isnull().sum())

# Mengecek duplikat data
print(data_day.duplicated().sum())
print(data_hour.duplicated().sum())

# Menggabungkan kedua dataset berdasarkan kolom 'dteday'
data = pd.concat([data_day, data_hour], axis=0)

# Menghilangkan kolom yang tidak diperlukan
columns_to_drop = ['instant', 'yr', 'holiday', 'weekday', 'casual', 'registered']
data = data.drop(columns_to_drop, axis=1)

# Menampilkan informasi tentang dataset setelah menghilangkan kolom
print(data.info())

# Menyimpan dataset yang sudah dibersihkan
data.to_csv('data_cleaned.csv', index=False)

# Load cleaned data
data = pd.read_csv('data_cleaned.csv')

# Sidebar
st.sidebar.title('Dashboard Penggunaan Bike Sharing')

# Menu selection
menu = st.sidebar.radio('Menu', ['Tren Penggunaan', 'Korelasi Cuaca', 'Pola Harian'])

if menu == 'Tren Penggunaan':
    st.header('Tren Penggunaan Bike Sharing')
    
    # Grafik Tren Penggunaan Sepeda Berdasarkan Bulan
    plt.figure(figsize=(10, 6))
    monthly_usage = data.groupby('mnth')['cnt'].mean()
    monthly_usage.plot(kind='line', marker='o', color='blue')
    plt.title('Tren Penggunaan Bike Sharing per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Rata-rata Peminjaman')
    plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
    plt.grid(True)
    st.pyplot(plt)

    # Grafik Tren Penggunaan Sepeda Berdasarkan Musim
    plt.figure(figsize=(8, 5))
    max_season = data.groupby('season')['cnt'].mean().idxmax()  
    colors = ['green' if season != max_season else 'red' for season in data['season'].unique()] 
    season_usage = data.groupby('season')['cnt'].mean()  
    season_usage.plot(kind='bar', color=colors)
    plt.title('Rata-rata Penggunaan Bike Sharing per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Rata-rata Peminjaman')
    plt.xticks(ticks=[0, 1, 2, 3], labels=['Musim Gugur', 'Musim Dingin', 'Musim Semi', 'Musim Panas'], rotation=45)
    st.pyplot(plt)

elif menu == 'Korelasi Cuaca':
    st.header('Korelasi antara Variabel Cuaca dan Penggunaan Bike Sharing')
    
    # Heatmap Korelasi
    plt.figure(figsize=(12, 8))
    weather_corr = data[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
    sns.heatmap(weather_corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Korelasi antara Variabel Cuaca dan Penggunaan Bike Sharing')
    st.pyplot(plt)

elif menu == 'Pola Harian':
    st.header('Pola Harian Penggunaan Bike Sharing')
    
    # Grafik Pola Penggunaan Sepeda Berdasarkan Jam
    plt.figure(figsize=(12, 6))
    hourly_usage = data.groupby('hr')['cnt'].mean()
    hourly_usage.plot(kind='bar', color='blue')
    plt.title('Rata-rata Penggunaan Bike Sharing per Jam')
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Jumlah Rata-rata Peminjaman')
    plt.xticks(rotation=0)
    st.pyplot(plt)

    # Perbedaan Pola Penggunaan antara Hari Kerja dan Akhir Pekan
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='hr', y='cnt', hue='workingday')
    plt.title('Perbedaan Pola Penggunaan Bike Sharing antara Hari Kerja dan Akhir Pekan')
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Jumlah Peminjaman')
    plt.xticks(rotation=0)
    plt.legend(title='Hari Kerja')
    st.pyplot(plt)
