import csv

class TrieNode:
    def __init__(self):
        self.children = {}  # Menyimpan anak nodes
        self.is_end_of_word = False  # Menandai akhir dari sebuah kata
        self.meaning = None  # Menyimpan arti dari kata (None jika bukan akhir kata)

class Trie:
    def __init__(self):
        self.root = TrieNode()  # Membuat root node

    # Method untuk memasukkan kata dan artinya ke dalam Trie
    def insert(self, word, meaning):
        current = self.root
        for char in word:
            # Jika karakter tidak ada di children, tambahkan node baru
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True  # Tandai akhir dari kata
        current.meaning = meaning  # Simpan arti kata
        print(f"Kata '{word}' dengan arti '{meaning}' berhasil dimasukkan")

    # Method untuk memeriksa apakah sebuah kata ada di dalam Trie dan mengembalikan artinya
    def search(self, word):
        current = self.root
        for char in word:
            # Jika karakter tidak ditemukan, kembalikan None
            if char not in current.children:
                return None
            current = current.children[char]
        if current.is_end_of_word:
            return current.meaning  # Kembalikan arti jika ini adalah akhir dari kata
        else:
            return None

    # Method untuk memeriksa apakah ada kata yang dimulai dengan prefix tertentu
    def starts_with(self, prefix):
        current = self.root
        for char in prefix:
            # Jika karakter tidak ditemukan, kembalikan False
            if char not in current.children:
                return False
            current = current.children[char]
        return True  # Kembalikan True jika prefix ditemukan

    # Method untuk menghapus kata dari Trie
    def delete(self, word):
        def _delete(current, word, index):
            # Basis rekursi: jika mencapai akhir kata
            if index == len(word):
                # Jika kata ini tidak benar-benar ada, tidak ada yang perlu dihapus
                if not current.is_end_of_word:
                    return False
                current.is_end_of_word = False
                current.meaning = None  # Hapus arti kata
                # Jika node ini tidak memiliki children, hapus node ini
                return len(current.children) == 0

            char = word[index]
            node = current.children.get(char)
            # Jika karakter tidak ada, tidak bisa menghapus
            if node is None:
                return False

            # Lanjutkan rekursi
            should_delete_current_node = _delete(node, word, index + 1)

            # Jika harus menghapus node saat ini, hapus dari children dictionary
            if should_delete_current_node:
                del current.children[char]
                # Kembalikan True jika tidak ada children lagi dan bukan akhir dari kata lain
                return len(current.children) == 0

            return False

        _delete(self.root, word, 0)

    # Method untuk menampilkan semua kata dalam Trie sesuai abjad
    def display_all_words(self):
        def _collect_words(node, prefix, words):
            # Jika node adalah akhir dari sebuah kata, tambahkan ke list
            if node.is_end_of_word:
                words.append((prefix, node.meaning))
            # Rekursi untuk setiap child node
            for char in sorted(node.children):
                _collect_words(node.children[char], prefix + char, words)

        words = []
        _collect_words(self.root, "", words)
        # Tampilkan kata-kata dengan artinya
        for word, meaning in words:
            print(f"Kata: '{word}', Arti: '{meaning}'")

    # Method untuk menyimpan Trie ke dalam file CSV
    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            self._write_node_to_csv(self.root, '', writer)
        print(f"Data berhasil disimpan ke dalam file {filename}")

    # Helper method untuk menulis node Trie ke file CSV
    def _write_node_to_csv(self, node, word, writer):
        if node.is_end_of_word:
            writer.writerow([word, node.meaning])
        for char, child_node in node.children.items():
            self._write_node_to_csv(child_node, word + char, writer)

    # Method untuk memuat Trie dari file CSV
    def load_from_csv(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    word, meaning = row
                    self.insert(word, meaning)
            print(f"Data berhasil dimuat dari file {filename}")
        except FileNotFoundError:
            print(f"File {filename} tidak ditemukan, memulai dengan Trie kosong.")

# Contoh penggunaan
trie = Trie()

# Memuat data dari CSV saat program dimulai
trie.load_from_csv('kamus.csv')

while True:
    print("\nWelcome")
    print("1. Masukkan kata baru")
    print("2. Cari kata")
    print("3. Cari kata berawalan karakter tertentu")
    print("4. Hapus kata")
    print("5. Tampilkan semua kata")
    print("6. Keluar")

    try:
        # Pastikan mengkonversi input menjadi integer
        choose = int(input("Masukkan pilihan anda [1-6]: "))
    except ValueError:
        print("Input tidak valid. Silakan masukkan angka antara 1-6.")
        continue  # Kembali ke awal loop jika input tidak valid

    if choose == 1:
        word = input("Masukkan kata baru: ")
        meaning = input("Masukkan arti kata: ")
        trie.insert(word, meaning)
    elif choose == 2:
        key = input("Masukkan kata yang ingin dicari: ")
        meaning = trie.search(key)
        if meaning:
            print(f"Kata '{key}' ditemukan dengan arti: '{meaning}'.")
        else:
            print(f"Kata '{key}' tidak ditemukan.")
    elif choose == 3:
        prefix = input("Masukkan prefix yang ingin dicari: ")
        if trie.starts_with(prefix):
            print(f"Ada kata yang berawalan dengan '{prefix}'.")
        else:
            print(f"Tidak ada kata yang berawalan dengan '{prefix}'.")
    elif choose == 4:
        word = input("Masukkan kata yang ingin dihapus: ")
        trie.delete(word)
        print(f"Kata '{word}' telah dihapus jika ada.")
    elif choose == 5:
        print("Menampilkan semua kata dalam Trie:")
        trie.display_all_words()
    elif choose == 6:
        print("Menyimpan data dan keluar dari program. Terima kasih!")
        trie.save_to_csv('kamus.csv')
        break  # Keluar dari loop
    else:
        print("Pilihan tidak valid. Silakan pilih antara 1-6.")
