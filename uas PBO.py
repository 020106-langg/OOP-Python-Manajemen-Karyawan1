from abc import ABC, abstractmethod
from collections import Counter


# Abstract Class untuk Karyawan
# Konsep OOP: Abstraction (Abstraksi)
class Karyawan(ABC):
    def __init__(self, nama, id_karyawan, departemen, gaji):
        # Konsep OOP: Encapsulation (Enkapsulasi)
        # Atribut privat untuk menyimpan data karyawan
        self.__nama = nama
        self.__id_karyawan = id_karyawan
        self.__departemen = departemen
        self.__gaji = gaji

    # Getter untuk nama (Encapsulation)
    def get_nama(self):
        return self.__nama

    # Getter untuk ID karyawan (Encapsulation)
    def get_id(self):
        return self.__id_karyawan

    # Getter untuk departemen (Encapsulation)
    def get_departemen(self):
        return self.__departemen

    # Getter untuk gaji (Encapsulation)
    def get_gaji(self):
        return self.__gaji

    # Setter untuk mengubah gaji (Encapsulation)
    def set_gaji(self, gaji_baru):
        self.__gaji = gaji_baru

    # Method abstrak untuk menghitung bonus (Abstraction & Polymorphism)
    @abstractmethod
    def hitung_bonus(self):
        pass

    # Menampilkan informasi lengkap karyawan
    def tampilkan_info(self):
        print(f"Nama       : {self.__nama}")
        print(f"ID         : {self.__id_karyawan}")
        print(f"Departemen : {self.__departemen}")
        print(f"Gaji       : Rp {self.__gaji:,}")
        print(f"Bonus      : Rp {self.hitung_bonus():,}")
        print("-" * 30)


# Subclass Manager
# Konsep OOP: Inheritance (Pewarisan)
class Manager(Karyawan):
    def __init__(self, nama, id_karyawan, departemen, gaji, jumlah_bawahan):
        # Memanggil konstruktor parent (Inheritance)
        super().__init__(nama, id_karyawan, departemen, gaji)
        self.__jumlah_bawahan = jumlah_bawahan

    # Override method hitung_bonus (Polymorphism)
    def hitung_bonus(self):
        # Bonus manager = 10% gaji + 50.000 x jumlah bawahan
        return int(self.get_gaji() * 0.10 + 50000 * self.__jumlah_bawahan)

    # Mengembalikan data ekstra (jumlah bawahan)
    def get_data_ekstra(self):
        return str(self.__jumlah_bawahan)


# Subclass Developer
# Konsep OOP: Inheritance (Pewarisan)
class Developer(Karyawan):
    def __init__(self, nama, id_karyawan, departemen, gaji, bahasa_pemrograman):
        # Memanggil konstruktor parent (Inheritance)
        super().__init__(nama, id_karyawan, departemen, gaji)
        self.__bahasa_pemrograman = bahasa_pemrograman

    # Override method hitung_bonus (Polymorphism)
    def hitung_bonus(self):
        # Bonus developer = 7% gaji + 100.000 jika Python/Java
        bonus = self.get_gaji() * 0.07
        if self.__bahasa_pemrograman.lower() in ['python', 'java']:
            bonus += 100000
        return int(bonus)

    # Mengembalikan data ekstra (bahasa pemrograman)
    def get_data_ekstra(self):
        return self.__bahasa_pemrograman

# Kelas Perusahaan untuk manajemen karyawan
# Konsep OOP: Aggregation (Agregasi)
class Perusahaan:
    def __init__(self, nama_perusahaan):
        self.nama_perusahaan = nama_perusahaan
        self.daftar_karyawan = []  # Menyimpan objek-objek Karyawan

    # Menambah karyawan baru, cek ID unik
    def tambah_karyawan(self, karyawan):
        # Exception Handling untuk ID unik
        if any(k.get_id() == karyawan.get_id() for k in self.daftar_karyawan):
            raise ValueError("ID karyawan sudah terdaftar.")
        self.daftar_karyawan.append(karyawan)

    # Menampilkan semua data karyawan
    def tampilkan_semua_karyawan(self):
        if not self.daftar_karyawan:
            print("Belum ada data karyawan.")
            return
        print(f"\nDaftar Karyawan di {self.nama_perusahaan}")
        print("=" * 40)
        for k in self.daftar_karyawan:
            k.tampilkan_info()

    # Mencari karyawan berdasarkan ID
    def cari_karyawan(self, id_karyawan):
        for k in self.daftar_karyawan:
            if k.get_id() == id_karyawan:
                return k
        return None

    # Menghapus karyawan berdasarkan ID
    def hapus_karyawan(self, id_karyawan):
        karyawan = self.cari_karyawan(id_karyawan)
        if karyawan:
            self.daftar_karyawan.remove(karyawan)
            print("Karyawan berhasil dihapus.")
        else:
            print("Karyawan tidak ditemukan.")

    # Mengupdate gaji karyawan
    def update_gaji(self, id_karyawan, gaji_baru):
        karyawan = self.cari_karyawan(id_karyawan)
        if karyawan:
            karyawan.set_gaji(gaji_baru)
            print("Gaji berhasil diperbarui.")
        else:
            print("Karyawan tidak ditemukan.")

    # Menampilkan statistik jumlah karyawan per departemen
    def statistik_departemen(self):
        if not self.daftar_karyawan:
            print("Belum ada data karyawan.")
            return
        dept_list = [k.get_departemen() for k in self.daftar_karyawan]
        statistik = Counter(dept_list)
        print("\nStatistik Karyawan per Departemen:")
        for dept, jumlah in statistik.items():
            print(f"- {dept}: {jumlah} orang")

    # Menyimpan data karyawan ke file (Persistence)
    def simpan_ke_file(self, nama_file):
        with open(nama_file, 'w') as f:
            for k in self.daftar_karyawan:
                jenis = "Manager" if isinstance(k, Manager) else "Developer"
                data = f"{jenis},{k.get_nama()},{k.get_id()},{k.get_departemen()},{k.get_gaji()},{k.get_data_ekstra()}\n"
                f.write(data)
        print(f"Data berhasil disimpan ke {nama_file}")

    # Memuat data karyawan dari file (Persistence & Exception Handling)
    def muat_dari_file(self, nama_file):
        try:
            with open(nama_file, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) != 6:
                        continue
                    jenis, nama, id_k, dept, gaji, ekstra = parts
                    if jenis.lower() == "manager":
                        k = Manager(nama, id_k, dept, int(gaji), int(ekstra))
                    elif jenis.lower() == "developer":
                        k = Developer(nama, id_k, dept, int(gaji), ekstra)
                    else:
                        continue
                    self.tambah_karyawan(k)
            print(f"Data berhasil dimuat dari {nama_file}")
        except FileNotFoundError:
            print("File tidak ditemukan.")
        except Exception as e:
            print("Gagal memuat data:", e)


# Menu CLI untuk interaksi pengguna
def menu():
    perusahaan = Perusahaan("PT Pema Global Energi (PGE)")

    while True:
        print("\n=== MENU PERUSAHAAN ===")
        print("1. Tambah Karyawan")
        print("2. Tampilkan Semua Karyawan")
        print("3. Cari Karyawan")
        print("4. Update Gaji Karyawan")
        print("5. Hapus Karyawan")
        print("6. Statistik Departemen")
        print("7. Simpan ke File")
        print("8. Muat dari File")
        print("9. Keluar")

        pilihan = input("Pilih menu (1-9): ").strip()

        if pilihan == '1':
            try:
                # Input data karyawan baru
                jenis = input("Jenis Karyawan (Manager/Developer): ").strip().lower()
                nama = input("Nama: ")
                id_k = input("ID Karyawan: ")
                dept = input("Departemen: ")
                gaji = int(input("Gaji: "))
                if jenis == 'manager':
                    bawahan = int(input("Jumlah Bawahan: "))
                    karyawan = Manager(nama, id_k, dept, gaji, bawahan)
                elif jenis == 'developer':
                    bahasa = input("Bahasa Pemrograman: ")
                    karyawan = Developer(nama, id_k, dept, gaji, bahasa)
                else:
                    print("Jenis tidak dikenali.")
                    continue
                perusahaan.tambah_karyawan(karyawan)
                print("✅ Karyawan berhasil ditambahkan.")
            except ValueError as e:
                print("❌ Error:", e)

        elif pilihan == '2':
            perusahaan.tampilkan_semua_karyawan()

        elif pilihan == '3':
            id_k = input("Masukkan ID karyawan: ")
            k = perusahaan.cari_karyawan(id_k)
            if k:
                k.tampilkan_info()
            else:
                print("Karyawan tidak ditemukan.")

        elif pilihan == '4':
            id_k = input("Masukkan ID karyawan: ")
            try:
                gaji_baru = int(input("Masukkan gaji baru: "))
                perusahaan.update_gaji(id_k, gaji_baru)
            except ValueError:
                print("Input gaji tidak valid.")

        elif pilihan == '5':
            id_k = input("Masukkan ID karyawan yang ingin dihapus: ")
            perusahaan.hapus_karyawan(id_k)

        elif pilihan == '6':
            perusahaan.statistik_departemen()

        elif pilihan == '7':
            perusahaan.simpan_ke_file("data_karyawan.txt")

        elif pilihan == '8':
            perusahaan.muat_dari_file("data_karyawan.txt")

        elif pilihan == '9':
            print("Terima kasih. Program selesai.")
            break

        else:
            print("Pilihan tidak valid.")


# Jalankan Program jika file ini dieksekusi langsung
if __name__ == "__main__":
    menu()