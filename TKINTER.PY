import sqlite3  # Modul untuk mengelola database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Modul untuk membuat GUI

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database SQLite
    cursor = conn.cursor()  # Membuat cursor untuk menjalankan perintah SQL
    cursor.execute('''  # Membuat tabel jika belum ada
        CREATE TABLE IF NOT EXISTS nilai_siswa(
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # Kolom ID sebagai primary key
            nama_siswa TEXT,  # Kolom untuk nama siswa
            biologi INTEGER,  # Kolom untuk nilai Biologi
            fisika INTEGER,  # Kolom untuk nilai Fisika
            inggris INTEGER,  # Kolom untuk nilai Inggris
            prediksi_fakultas TEXT  # Kolom untuk prediksi fakultas
        )
    ''')
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute("SELECT * FROM nilai_siswa")  # Query untuk mengambil semua data
    rows = cursor.fetchall()  # Mengambil hasil query
    conn.close()  # Menutup koneksi
    return rows  # Mengembalikan data

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute('''  # Menyisipkan data baru ke tabel
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute('''  # Memperbarui data berdasarkan ID
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan ID
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  # Jika nilai Biologi paling tinggi
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:  # Jika nilai Fisika paling tinggi
        return "Teknik"
    elif inggris > biologi and inggris > fisika:  # Jika nilai Inggris paling tinggi
        return "Bahasa"
    else:  # Jika nilai sama atau tidak memenuhi kondisi di atas
        return "Tidak diketahui"

# Fungsi untuk menambahkan data baru
def submit():
    try:
        nama = nama_var.get()  # Mengambil input nama siswa
        biologi = int(biologi_var.get())  # Mengambil input nilai Biologi
        fisika = int(fisika_var.get())  # Mengambil input nilai Fisika
        inggris = int(inggris_var.get())  # Mengambil input nilai Inggris

        if not nama:  # Validasi jika nama kosong
            raise ValueError("Nama siswa tidak boleh kosong!")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Notifikasi sukses
        clear_input()  # Bersihkan input
        populate_table()  # Perbarui tabel
    except ValueError as e:  # Tangani kesalahan input
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data yang dipilih
def update():
    try:
        if not selected_record_id.get():  # Validasi jika tidak ada data yang dipilih
            raise ValueError("Pilih data dari tabel untuk diupdate!")
        record_id = int(selected_record_id.get())  # Ambil ID data yang dipilih
        nama = nama_var.get()  # Ambil input nama
        biologi = int(biologi_var.get())  # Ambil input nilai Biologi
        fisika = int(fisika_var.get())  # Ambil input nilai Fisika
        inggris = int(inggris_var.get())  # Ambil input nilai Inggris

        if not nama:  # Validasi jika nama kosong
            raise ValueError("Nama siswa tidak boleh kosong!")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Perbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Notifikasi sukses
        clear_input()  # Bersihkan input
        populate_table()  # Perbarui tabel
    except ValueError as e:  # Tangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data yang dipilih
def delete():
    try:
        if not selected_record_id.get():  # Validasi jika tidak ada data yang dipilih
            raise ValueError("Pilih data dari tabel untuk dihapus!")
        record_id = int(selected_record_id.get())  # Ambil ID data yang dipilih
        delete_database(record_id)  # Hapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Notifikasi sukses
        clear_input()  # Bersihkan input
        populate_table()  # Perbarui tabel
    except ValueError as e:  # Tangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk membersihkan input
def clear_input():
    nama_var.set("")  # Kosongkan input nama
    biologi_var.set("")  # Kosongkan input nilai Biologi
    fisika_var.set("")  # Kosongkan input nilai Fisika
    inggris_var.set("")  # Kosongkan input nilai Inggris
    selected_record_id.set("")  # Kosongkan ID data yang dipilih

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  # Hapus semua data di tabel
        tree.delete(row)
    for row in fetch_data():  # Tambahkan data dari database ke tabel
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi input dari data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Ambil item yang dipilih
        selected_row = tree.item(selected_item)['values']  # Ambil data dari item yang dipilih

        selected_record_id.set(selected_row[0])  # Set ID data yang dipilih
        nama_var.set(selected_row[1])  # Set nama siswa
        biologi_var.set(selected_row[2])  # Set nilai Biologi
        fisika_var.set(selected_row[3])  # Set nilai Fisika
        inggris_var.set(selected_row[4])  # Set nilai Inggris
    except IndexError:  # Tangani jika tidak ada data yang valid
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database dan GUI
create_database()  # Membuat database jika belum ada

root = Tk()  # Membuat jendela utama
root.title("Prediksi Fakultas Siswa")  # Judul jendela

# Variabel untuk input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# Membuat label dan entry untuk input data
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol untuk menambahkan, memperbarui, dan menghapus data
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")  # Kolom tabel
tree = ttk.Treeview(root, columns=columns, show='headings')  # Membuat tabel

for col in columns:  # Membuat header kolom
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menempatkan tabel di grid
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Bind event klik pada tabel

populate_table()  # Isi tabel dengan data dari database
root.mainloop()  # Jalankan aplikasi GUI
