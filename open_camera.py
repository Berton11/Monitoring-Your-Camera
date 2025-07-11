# Mengimpor library yang diperlukan
import tkinter as tk  # Untuk membuat antarmuka grafis (GUI)
from tkinter import ttk  # Untuk menggunakan widget GUI yang lebih modern
import cv2  # OpenCV untuk pemrosesan gambar dan video dari kamera
from PIL import Image, ImageTk  # Pillow untuk konversi gambar agar kompatibel dengan Tkinter

# Mengimpor fungsi untuk membuka koneksi kamera dari file lain
from open_camera_list import CAMERA_A, CAMERA_B, CAMERA_C, CAMERA_D

# Mendefinisikan kelas utama untuk aplikasi kamera
class CameraApp:
    # Metode inisialisasi, dieksekusi saat objek CameraApp dibuat
    def __init__(self, root):
        # =================================================================
        # === PENGATURAN JENDELA UTAMA DAN VARIABEL DASAR
        # =================================================================
        self.root = root  # Menyimpan referensi ke jendela utama Tkinter
        self.root.title("Monitoring CCTV")  # Mengatur judul jendela
        self.root.geometry("1300x600")  # Mengatur ukuran awal jendela
        self.display_size = (640, 480)  # Ukuran standar untuk menampilkan setiap video

        # =================================================================
        # === PEMBUATAN STRUKTUR GUI UNTUK SCROLLBAR
        # =================================================================
        # Membuat frame utama sebagai wadah untuk canvas dan scrollbar
        container = ttk.Frame(root)

        # Membuat Canvas, tempat konten (video) akan digambar dan bisa digulir
        canvas = tk.Canvas(container)
        # Membuat Scrollbar vertikal dan menghubungkan perintahnya ke fungsi yview dari canvas
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        # Membuat frame di dalam canvas yang akan menampung semua widget video
        self.scrollable_frame = ttk.Frame(canvas)

        # Mengikat (bind) event <Configure> pada scrollable_frame
        # Saat ukuran frame berubah, lambda function ini akan dijalankan
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")  # Mengatur ulang area scroll agar sesuai ukuran konten
            )
        )

        # Menempatkan scrollable_frame di dalam canvas pada posisi (0,0)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        # Menghubungkan scrollbar ke canvas (agar canvas bisa dikontrol scrollbar)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Menampilkan canvas dan scrollbar di dalam container
        canvas.pack(side="left", fill="both", expand=True)  # Canvas mengisi ruang kiri
        scrollbar.pack(side="right", fill="y")  # Scrollbar di sisi kanan, mengisi secara vertikal

        # Menampilkan tombol keluar dan container utama di jendela root
        quit_button = ttk.Button(root, text="Keluar", command=self.on_close)  # Membuat tombol keluar
        quit_button.pack(side=tk.BOTTOM, pady=10)  # Menempatkan tombol di bagian bawah
        container.pack(fill="both", expand=True, padx=10, pady=10)  # Container mengisi sisa ruang

        # =================================================================
        # === INISIALISASI DAN PEMBUKAAN KAMERA
        # =================================================================
        print("Membuka Kamera..")  # Pesan status di konsol
        # Menginisialisasi variabel penampung koneksi kamera ke None
        self.cap_a, self.cap_b, self.cap_c, self.cap_d = None, None, None, None
        # Membuka koneksi ke masing-masing kamera
        self.cap_a = CAMERA_A()
        self.cap_b = CAMERA_B()
        self.cap_c = CAMERA_C()
        self.cap_d = CAMERA_D()

        # Memeriksa apakah semua kamera berhasil dibuka
        if not all([self.cap_a.isOpened(), self.cap_b.isOpened(), self.cap_c.isOpened(), self.cap_d.isOpened()]):
            # Jika ada yang gagal, tampilkan pesan error di jendela utama
            error_label = ttk.Label(self.root, text="Satu atau lebih kamera tidak dapat dibuka")
            error_label.pack(pady=50, padx=20)
            self.on_close()  # Panggil fungsi on_close untuk membersihkan koneksi yang sudah ada
            return  # Hentikan proses inisialisasi lebih lanjut

        # =================================================================
        # === PENGATURAN TATA LETAK GRID UNTUK VIDEO
        # =================================================================
        # Mengatur agar kolom 0 dan 1 bisa melebar saat ukuran jendela diubah
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        # --- Tata Letak CAMERA_A ---
        # Membuat label judul untuk CAMERA_A dan menempatkannya di grid
        ttk.Label(self.scrollable_frame, text="CAMERA_A", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=5)
        # Membuat panel (label) untuk menampilkan video dari CAMERA_A
        self.panel_a = ttk.Label(self.scrollable_frame)
        # Menempatkan panel video di grid, di bawah judulnya
        self.panel_a.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # --- Tata Letak CAMERA_B ---
        # Membuat label judul untuk CAMERA_B dan menempatkannya di grid
        ttk.Label(self.scrollable_frame, text="CAMERA_B", font=("Helvetica", 12, "bold")).grid(row=0, column=1, pady=5)
        # Membuat panel untuk menampilkan video dari CAMERA_B
        self.panel_b = ttk.Label(self.scrollable_frame)
        # Menempatkan panel video di grid, di bawah judulnya
        self.panel_b.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # --- Tata Letak CAMERA_C ---
        # Membuat label judul untuk CAMERA_C dan menempatkannya di grid
        ttk.Label(self.scrollable_frame, text="CAMERA_C", font=("Helvetica", 12, "bold")).grid(row=2, column=0, columnspan=1, pady=(5, 5))
        # Membuat panel untuk menampilkan video dari CAMERA_C
        self.panel_c = ttk.Label(self.scrollable_frame)
        # Menempatkan panel video di grid, di bawah judulnya
        self.panel_c.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)

        # --- Tata Letak CAMERA_D ---
        # Membuat label judul untuk CAMERA_D dan menempatkannya di grid
        ttk.Label(self.scrollable_frame, text="CAMERA_D", font=("Helvetica", 12, "bold")).grid(row=2, column=1, pady=(5, 5))
        # Membuat panel untuk menampilkan video dari CAMERA_D
        self.panel_d = ttk.Label(self.scrollable_frame)
        # Menempatkan panel video di grid, di bawah judulnya
        self.panel_d.grid(row=3, column=1, columnspan=1, sticky="nsew", padx=3, pady=3)

        # =================================================================
        # === MEMULAI PROSES PEMBARUAN FRAME
        # =================================================================
        self.update_frame()  # Memanggil fungsi update_frame untuk pertama kali
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Mengatur agar fungsi on_close dipanggil saat jendela ditutup

    # Metode untuk memperbarui frame video secara terus-menerus
    def update_frame(self):

        # --- Proses Frame CAMERA_A ---
        ret_a, frame_a = self.cap_a.read()  # Membaca satu frame dari kamera A
        if ret_a:  # Jika frame berhasil dibaca
            frame_a_resized = cv2.resize(frame_a, self.display_size)  # Mengubah ukuran frame
            image_rgb_a = cv2.cvtColor(frame_a_resized, cv2.COLOR_BGR2RGB)  # Konversi warna BGR ke RGB
            image_pil_a = Image.fromarray(image_rgb_a)  # Buat objek gambar PIL
            imagetk_a = ImageTk.PhotoImage(image=image_pil_a)  # Buat objek gambar Tkinter
            self.panel_a.imgtk = imagetk_a  # Simpan referensi gambar agar tidak hilang dari memori
            self.panel_a.config(image=imagetk_a)  # Tampilkan gambar di panel A

        # --- Proses Frame CAMERA_B ---
        ret_b, frame_b = self.cap_b.read()  # Membaca satu frame dari kamera B
        # Memeriksa status dari variabel 'ret_office1' (TERDAPAT KESALAHAN: seharusnya 'ret_b')
        if ret_office1:
            frame_b_resized = cv2.resize(frame_b, self.display_size)  # Mengubah ukuran frame
            image_rgb_b = cv2.cvtColor(frame_b_resized, cv2.COLOR_BGR2RGB)  # Konversi warna BGR ke RGB
            image_pil_b = Image.fromarray(image_rgb_b)  # Buat objek gambar PIL
            imgtk_b = ImageTk.PhotoImage(image=image_pil_b)  # Buat objek gambar Tkinter
            self.panel_b.imgtk = imgtk_b  # Simpan referensi gambar
            self.panel_b.config(image=imgtk_b)  # Tampilkan gambar di panel B

        # --- Proses Frame CAMERA_C ---
        ret_c, frame_c = self.cap_c.read()  # Membaca satu frame dari kamera C
        if ret_c:  # Jika frame berhasil dibaca
            frame_c_resized = cv2.resize(frame_c, self.display_size)  # Mengubah ukuran frame
            image_rgb_c = cv2.cvtColor(frame_c_resized, cv2.COLOR_BGR2RGB)  # Konversi warna BGR ke RGB
            image_pil_c = Image.fromarray(image_rgb_c)  # Buat objek gambar PIL
            # Membuat gambar Tkinter dari variabel 'image_pil_office2' (TERDAPAT KESALAHAN: seharusnya 'image_pil_c')
            imgtk_c = ImageTk.PhotoImage(image=image_pil_office2)
            self.panel_c.imgtk = imgtk_c  # Simpan referensi gambar
            self.panel_c.config(image=imgtk_c)  # Tampilkan gambar di panel C

        # --- Proses Frame CAMERA_D ---
        ret_d, frame_d = self.cap_d.read()  # Membaca satu frame dari kamera D
        # Memeriksa status dari variabel 'ret_machine' (TERDAPAT KESALAHAN: seharusnya 'ret_d')
        if ret_machine:
            d_resize = cv2.resize(frame_d, self.display_size)  # Mengubah ukuran frame
            image_rgb_d = cv2.cvtColor(d_resize, cv2.COLOR_BGR2RGB)  # Konversi warna BGR ke RGB
            image_pil_d = Image.fromarray(image_rgb_d)  # Buat objek gambar PIL
            imgtk_d = ImageTk.PhotoImage(image=image_pil_d)  # Buat objek gambar Tkinter
            self.panel_d.imgtk = imgtk_d  # Simpan referensi gambar
            self.panel_d.config(image=imgtk_d)  # Tampilkan gambar di panel D

        # Menjadwalkan fungsi update_frame untuk dijalankan lagi setelah 15 milidetik
        self.root.after(15, self.update_frame)

    # Metode untuk menutup aplikasi dengan aman
    def on_close(self):
        print("--- Menutup semua koneksi kamera dan aplikasi ---")  # Pesan status di konsol
        # --- Melepaskan semua koneksi kamera satu per satu dengan aman ---
        # Memeriksa jika atribut ada dan kamera terbuka sebelum melepaskannya
        if hasattr(self, 'cap_a') and self.cap_a and self.cap_a.isOpened():
            self.cap_a.release()
        if hasattr(self, 'cap_b') and self.cap_b and self.cap_b.isOpened():
            self.cap_b.release()
        if hasattr(self, 'cap_c') and self.cap_c and self.cap_c.isOpened():
            self.cap_c.release()
        if hasattr(self, 'cap_d') and self.cap_d and self.cap_d.isOpened():
            self.cap_d.release()

        # Memeriksa jika jendela utama masih ada sebelum menutupnya
        if self.root:
            self.root.destroy()  # Menutup jendela dan menghentikan aplikasi
            self.root = None  # Mengatur referensi ke None untuk menghindari error

# =================================================================
# === TITIK MASUK UTAMA PROGRAM
# =================================================================
# Blok ini hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    root = tk.Tk()  # Membuat jendela utama aplikasi
    app = CameraApp(root)  # Membuat instance dari kelas CameraApp
    root.mainloop()  # Memulai event loop Tkinter, aplikasi mulai berjalan dan menunggu interaksi
