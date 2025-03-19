import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import base64
import zlib
import os
import re
from pathlib import Path
# Developed by WONG © 2023-2024
import marshal
import binascii
import random
import string
import codecs
import struct
import types
import sv_ttk  # Developed by WONG © 2023-2024
from tkinter import font

class ModernGlassApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Encoder/Decoder/Obfuscator")
        self.geometry("950x650")
        self.configure(bg="#f5f5f7")
        
        # Gunakan Sun Valley theme untuk tampilan modern
        sv_ttk.set_theme("light")
        
        # Kustomisasi font
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=10)
        
        # Inisialisasi aplikasi
        self.app = EncoderDecoderApp(self)
        
        # Buat efek transparan untuk area tertentu
        self.bind("<Map>", self.setup_glass_effect)
    
    def setup_glass_effect(self, event=None):
        # Fungsi ini akan dipanggil saat jendela tampil
        # Kita bisa menambahkan efek glass seperti blur dan transparansi disini
        pass

class EncoderDecoderApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        # Konfigurasi tema modern glass
        self.style = ttk.Style()
        
        # Konfigurasi style untuk komponen
        self.style.configure('Glass.TFrame', background='#ffffff10', borderwidth=0)
        self.style.configure('Card.TFrame', background='#ffffff', borderwidth=0, relief='flat')
        self.style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), foreground='#ffffff')
        self.style.configure('Modern.TLabel', background='#f5f5f7', font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', background='#f5f5f7', font=('Segoe UI', 14, 'bold'))
        self.style.configure('Subtitle.TLabel', background='#f5f5f7', font=('Segoe UI', 11))
        
        # Main container
        main_container = ttk.Frame(self.root, style='TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header dengan gradient
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        app_title = ttk.Label(header_frame, text="PYTHON CODE PROCESSOR", style='Title.TLabel')
        app_title.pack(anchor=tk.W)
        
        app_subtitle = ttk.Label(header_frame, text="Encode • Decode • Obfuscate", style='Subtitle.TLabel')
        app_subtitle.pack(anchor=tk.W)
        
        # Frame utama dengan efek card
        main_card = ttk.Frame(main_container, style='Card.TFrame')
        main_card.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)
        main_card.configure(padding=(20, 20, 20, 20))
        
        # Frame file selection dengan desain modern
        file_frame = ttk.Frame(main_card)
        file_frame.pack(fill=tk.X, pady=15)
        
        file_label = ttk.Label(file_frame, text="File Python", style='Modern.TLabel')
        file_label.pack(anchor=tk.W, pady=(0, 5))
        
        file_input_frame = ttk.Frame(file_frame)
        file_input_frame.pack(fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_input_frame, textvariable=self.file_path_var, width=70)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        
        browse_button = ttk.Button(file_input_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Separator
        separator = ttk.Separator(main_card, orient='horizontal')
        separator.pack(fill=tk.X, pady=15)
        
        # Mode selection dengan desain modern
        mode_frame = ttk.Frame(main_card)
        mode_frame.pack(fill=tk.X, pady=5)
        
        mode_label = ttk.Label(mode_frame, text="Processing Mode", style='Modern.TLabel')
        mode_label.pack(anchor=tk.W, pady=(0, 10))
        
        mode_buttons_frame = ttk.Frame(mode_frame)
        mode_buttons_frame.pack(fill=tk.X)
        
        self.mode_var = tk.StringVar(value="encode")
        
        # Modern tab-like radio buttons
        encode_radio_frame = ttk.Frame(mode_buttons_frame)
        encode_radio_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        encode_radio = ttk.Radiobutton(encode_radio_frame, text="Encode/Decode", value="encode", 
                                       variable=self.mode_var, command=self.update_options)
        encode_radio.pack(pady=5)
        
        self.encode_indicator = ttk.Frame(encode_radio_frame, height=2)
        self.encode_indicator.pack(fill=tk.X)
        
        obfuscate_radio_frame = ttk.Frame(mode_buttons_frame)
        obfuscate_radio_frame.pack(side=tk.LEFT)
        
        obfuscate_radio = ttk.Radiobutton(obfuscate_radio_frame, text="Obfuscate", value="obfuscate", 
                                          variable=self.mode_var, command=self.update_options)
        obfuscate_radio.pack(pady=5)
        
        self.obfuscate_indicator = ttk.Frame(obfuscate_radio_frame, height=2)
        self.obfuscate_indicator.pack(fill=tk.X)
        
        # Options container
        options_container = ttk.Frame(main_card)
        options_container.pack(fill=tk.X, pady=15)
        
        # Options frame - akan diperbarui sesuai mode
        self.options_frame = ttk.Frame(options_container)
        self.options_frame.pack(fill=tk.X)
        
        # Encode/Decode options dengan desain modern
        self.encode_options_frame = ttk.Frame(self.options_frame)
        
        layers_label = ttk.Label(self.encode_options_frame, text="Jumlah Lapisan Encoding", style='Modern.TLabel')
        layers_label.pack(anchor=tk.W, pady=(0, 5))
        
        layers_frame = ttk.Frame(self.encode_options_frame)
        layers_frame.pack(fill=tk.X)
        
        self.layers_var = tk.IntVar(value=1)
        layers_spinbox = ttk.Spinbox(layers_frame, from_=1, to=5, textvariable=self.layers_var, width=5)
        layers_spinbox.pack(side=tk.LEFT)
        
        # Obfuscate options dengan desain modern
        self.obfuscate_options_frame = ttk.Frame(self.options_frame)
        
        obfuscate_method_label = ttk.Label(self.obfuscate_options_frame, text="Metode Obfuscation", style='Modern.TLabel')
        obfuscate_method_label.pack(anchor=tk.W, pady=(0, 5))
        
        obfuscate_method_frame = ttk.Frame(self.obfuscate_options_frame)
        obfuscate_method_frame.pack(fill=tk.X)
        
        self.obfuscate_method_var = tk.StringVar(value="Marshal")
        obfuscate_methods = ttk.Combobox(obfuscate_method_frame, textvariable=self.obfuscate_method_var, width=20, state="readonly")
        obfuscate_methods['values'] = ("Marshal", "Strong Obfuscation", "Super Complex")
        obfuscate_methods.pack(side=tk.LEFT)
        
        # Action buttons dengan desain modern glass
        actions_container = ttk.Frame(main_card)
        actions_container.pack(fill=tk.X, pady=20)
        
        # Left frame for specific operation buttons
        self.operation_buttons_frame = ttk.Frame(actions_container)
        self.operation_buttons_frame.pack(side=tk.LEFT)
        
        # Encode/Decode buttons
        self.encode_buttons_frame = ttk.Frame(self.operation_buttons_frame)
        
        encode_button = ttk.Button(self.encode_buttons_frame, text="Encode", 
                                  command=self.encode_file, style='Accent.TButton')
        encode_button.pack(side=tk.LEFT, padx=(0, 10))
        
        decode_button = ttk.Button(self.encode_buttons_frame, text="Decode", 
                                  command=self.decode_file)
        decode_button.pack(side=tk.LEFT)
        
        # Obfuscate button
        self.obfuscate_buttons_frame = ttk.Frame(self.operation_buttons_frame)
        
        obfuscate_button = ttk.Button(self.obfuscate_buttons_frame, text="Obfuscate", 
                                     command=self.obfuscate_file, style='Accent.TButton')
        obfuscate_button.pack(side=tk.LEFT)
        
        # Right frame for the universal OK button
        ok_frame = ttk.Frame(actions_container)
        ok_frame.pack(side=tk.RIGHT)
        
        ok_button = ttk.Button(ok_frame, text="Process", width=15, 
                              command=self.execute_selected_operation, style='Accent.TButton')
        ok_button.pack()
        
        # Tampilkan frame yang sesuai dengan mode awal
        self.update_options()
        
        # Output area dengan desain modern glass
        output_container = ttk.Frame(main_container)
        output_container.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        output_header_frame = ttk.Frame(output_container)
        output_header_frame.pack(fill=tk.X, pady=(0, 10))
        
        output_label = ttk.Label(output_header_frame, text="Output Log", style='Subtitle.TLabel')
        output_label.pack(anchor=tk.W)
        
        output_frame = ttk.Frame(output_container, style='Card.TFrame')
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(output_frame, height=10, width=70, borderwidth=0,
                                  font=('Consolas', 10), bg='#ffffff')
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        scrollbar = ttk.Scrollbar(self.output_text, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        
        # Status bar dengan desain modern
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_var = tk.StringVar(value="Siap memproses file")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, style='Modern.TLabel')
        status_bar.pack(anchor=tk.W)
    
    def update_options(self):
        """Update tampilan opsi berdasarkan mode yang dipilih"""
        mode = self.mode_var.get()
        
        # Update indikator tab aktif - PERBAIKAN DISINI
        if mode == "encode":
            # Buat style khusus untuk indikator
            self.style.configure('Active.TFrame', background='#007bff')
            self.style.configure('Inactive.TFrame', background='#f5f5f7')
            self.encode_indicator.configure(style='Active.TFrame')
            self.obfuscate_indicator.configure(style='Inactive.TFrame')
        else:
            self.style.configure('Active.TFrame', background='#007bff')
            self.style.configure('Inactive.TFrame', background='#f5f5f7')
            self.encode_indicator.configure(style='Inactive.TFrame')
            self.obfuscate_indicator.configure(style='Active.TFrame')
        
        # Hapus frame yang ditampilkan sebelumnya
        for widget in self.options_frame.winfo_children():
            widget.pack_forget()
        
        # Hapus tombol aksi yang ditampilkan sebelumnya
        self.encode_buttons_frame.pack_forget()
        self.obfuscate_buttons_frame.pack_forget()
        
        # Tampilkan opsi yang sesuai
        if mode == "encode":
            self.encode_options_frame.pack(fill=tk.X)
            self.encode_buttons_frame.pack()
        else:
            self.obfuscate_options_frame.pack(fill=tk.X)
            self.obfuscate_buttons_frame.pack()
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            self.file_path_var.set(file_path)
            self.status_var.set(f"File dipilih: {os.path.basename(file_path)}")
    
    def encode_file(self):
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showerror("Error", "Silakan pilih file Python terlebih dahulu.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File tidak ditemukan.")
            return
        
        try:
            layers = self.layers_var.get()
            if layers < 1 or layers > 5:
                messagebox.showerror("Error", "Jumlah lapisan harus antara 1 dan 5.")
                return
            
            # Baca file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Encode
            encoded_content = self.encode_content(content, layers)
            
            # Simpan ke file baru
            output_path = self.generate_output_filename(file_path, "_encoded")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(encoded_content)
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"✅ File berhasil dienkode dengan {layers} lapis.\n\n", "success")
            self.output_text.insert(tk.END, f"📂 Tersimpan di: {output_path}\n\n")
            self.output_text.insert(tk.END, "📝 Berikut sampel dari konten yang dienkode:\n\n")
            self.output_text.insert(tk.END, encoded_content[:200] + "...\n")
            
            # Atur tag untuk text styling
            self.output_text.tag_configure("success", foreground="#28a745")
            
            self.status_var.set(f"File berhasil dienkode: {os.path.basename(output_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengenkode file: {str(e)}")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"❌ ERROR: {str(e)}", "error")
            self.output_text.tag_configure("error", foreground="#dc3545")
            self.status_var.set("Error saat mengenkode file")
    
    def decode_file(self):
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showerror("Error", "Silakan pilih file Python terlebih dahulu.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File tidak ditemukan.")
            return
        
        try:
            # Baca file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Deteksi jumlah lapisan
            layers = self.detect_encoding_layers(content)
            if layers == 0:
                messagebox.showerror("Error", "File tidak terenkode atau format tidak dikenali.")
                return
            
            # Decode
            decoded_content = self.decode_content(content, layers)
            
            # Simpan ke file baru
            output_path = self.generate_output_filename(file_path, "_decoded")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(decoded_content)
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"✅ File berhasil didekode dari {layers} lapis.\n\n", "success")
            self.output_text.insert(tk.END, f"📂 Tersimpan di: {output_path}\n\n")
            self.output_text.insert(tk.END, "📝 Berikut sampel dari konten yang didekode:\n\n")
            self.output_text.insert(tk.END, decoded_content[:200] + "...\n")
            
            # Atur tag untuk text styling
            self.output_text.tag_configure("success", foreground="#28a745")
            
            self.status_var.set(f"File berhasil didekode: {os.path.basename(output_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mendekode file: {str(e)}")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"❌ ERROR: {str(e)}", "error")
            self.output_text.tag_configure("error", foreground="#dc3545")
            self.status_var.set("Error saat mendekode file")
    
    def obfuscate_file(self):
        """Obfuscate file Python menggunakan metode yang dipilih"""
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showerror("Error", "Silakan pilih file Python terlebih dahulu.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File tidak ditemukan.")
            return
        
        try:
            method = self.obfuscate_method_var.get().lower()
            
            # Baca dan obfuscate
            obfuscated_content = ""
            if method == "marshal":
                obfuscated_content = self.obfuscate_with_marshal(file_path)
            elif method == "strong obfuscation":
                obfuscated_content = self.strong_obfuscate(file_path)
            elif method == "super complex":
                obfuscated_content = self.strong_complex_obfuscate(file_path)
            else:
                messagebox.showerror("Error", "Metode obfuscation tidak valid.")
                return
            
            # Simpan ke file baru
            output_path = self.generate_output_filename(file_path, "_obfuscated")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(obfuscated_content)
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"✅ File berhasil diobfuskasi dengan metode {method}.\n\n", "success")
            self.output_text.insert(tk.END, f"📂 Tersimpan di: {output_path}\n\n")
            self.output_text.insert(tk.END, "⚠️ PERINGATAN: File yang diobfuskasi tidak dapat didekode kembali!\n\n", "warning")
            self.output_text.insert(tk.END, "📝 Berikut sampel dari konten yang diobfuskasi:\n\n")
            self.output_text.insert(tk.END, obfuscated_content[:200] + "...\n")
            
            # Developed by WONG © 2023-2024
            self.output_text.tag_configure("success", foreground="#28a745")
            self.output_text.tag_configure("warning", foreground="#fd7e14")
            
            self.status_var.set(f"File berhasil diobfuskasi: {os.path.basename(output_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengobfuskasi file: {str(e)}")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"❌ ERROR: {str(e)}", "error")
            self.output_text.tag_configure("error", foreground="#dc3545")
            self.status_var.set("Error saat mengobfuskasi file")
        
    def encode_content(self, content, layers):
        # Basis untuk encoding
        template = '''
# Encoded Python
import base64
import zlib

def decode(code, layers={}):
    for _ in range(layers):
        code = zlib.decompress(base64.b64decode(code.encode())).decode()
    return code

encoded_code = "{}"

exec(decode(encoded_code, {}))
'''
        # Enkode file
        encoded = content
        for _ in range(layers):
            compressed = zlib.compress(encoded.encode())
            encoded = base64.b64encode(compressed).decode()
        
        # Hasilkan file yang dapat dijalankan
        return template.format(layers, encoded, layers)
    
    def decode_content(self, content, layers):
        # Cari encoded_code
        pattern = r'encoded_code\s*=\s*[\'"]([^\'"]+)[\'"]'
        match = re.search(pattern, content)
        
        if not match:
            raise ValueError("Format file terenkode tidak valid")
        
        encoded = match.group(1)
        
        # Dekode konten
        for _ in range(layers):
            decoded_bytes = base64.b64decode(encoded.encode())
            decoded = zlib.decompress(decoded_bytes).decode()
            encoded = decoded
        
        return decoded
    
    def detect_encoding_layers(self, content):
        # Deteksi berapa lapisan encoding
        pattern = r'layers\s*=\s*(\d+)'
        match = re.search(pattern, content)
        
        if match:
            return int(match.group(1))
        
        return 0
    
    def obfuscate_with_marshal(self, file_path):
        """Obfuskasi menggunakan marshal - tidak bisa didekode tapi tetap bisa dijalankan"""
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Kompilasi kode Python
        compiled_code = compile(code, '<string>', 'exec')
        
        # Marshal compile code (binary format)
        marshalled = marshal.dumps(compiled_code)
        
        # Base64 untuk membuatnya printable
        encoded = base64.b64encode(marshalled).decode()
        
        # Template untuk menjalankan kode yang sudah diobfuskasi
        template = f'''
# Obfuscated Python - Tidak bisa didekode kembali
import base64
import marshal
import zlib

# Kode terobfuskasi - tidak bisa diekstrak kembali
exec(marshal.loads(base64.b64decode({repr(encoded)})))
'''
        return template
    
    def strong_obfuscate(self, file_path):
        """Metode obfuskasi kompleks dengan beberapa lapisan"""
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Kompilasi kode
        compiled_code = compile(code, '<string>', 'exec')
        marshalled = marshal.dumps(compiled_code)
        
        # Kompresi dan enkripsi dasar
        compressed = zlib.compress(marshalled)
        encoded = base64.b85encode(compressed)
        
        # Tambahkan "salt" acak untuk mempersulit reverse engineering
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        xored_data = bytes([b ^ ord(salt[i % len(salt)]) for i, b in enumerate(encoded)])
        
        # Konversi ke hex untuk membuatnya lebih sulit dibaca
        hex_data = binascii.hexlify(xored_data).decode()
        
        # Template untuk dekode dan eksekusi
        template = f'''
# PERINGATAN: Kode ini sengaja diobfuskasi dan tidak dapat didekode
import base64, marshal, zlib, binascii

_={repr(salt)}
__=binascii.unhexlify("{hex_data}")
___=bytes([b ^ ord(_[i % len(_)]) for i, b in enumerate(__)])
____=zlib.decompress(base64.b85decode(___))
exec(marshal.loads(____))
'''
        return template
    
    def strong_complex_obfuscate(self, file_path):
        """Metode obfuskasi super kompleks dengan banyak lapisan"""
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Kompilasi kode Python
        compiled_code = compile(code, '<string>', 'exec')
        
        # Buat kunci acak
        complex_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        
        # Marshal compile code
        marshalled = marshal.dumps(compiled_code)
        
        # Lakukan kompresi
        compressed = zlib.compress(marshalled, 9)  # Kompresi level 9 (maksimum)
        
        # Lakukan transformasi kompleks
        # 1. Encode dengan base85 (lebih efisien dari base64)
        b85_encoded = base64.b85encode(compressed)
        
        # 2. XOR dengan kunci
        xored_data = bytes([b ^ ord(complex_key[i % len(complex_key)]) for i, b in enumerate(b85_encoded)])
        
        # 3. Encode dengan hexlify
        hex_data = binascii.hexlify(xored_data)
        
        # 4. Pembalikan urutan byte
        reversed_data = hex_data[::-1]
        
        # 5. Encode lagi dengan base64 untuk keamanan tambahan
        final_encoded = base64.b64encode(reversed_data).decode()
        
        # Buat template yang menyertakan semua transformasi untuk decode
        template = f'''
# Super Complex Obfuscated Python - Cannot be decoded back to source
import base64, zlib, marshal, binascii, codecs, types, struct

def _decode_and_execute(encoded_data, key):
    # 1. Decode base64
    step1 = base64.b64decode(encoded_data)
    
    # 2. Reverse bytes
    step2 = step1[::-1]
    
    # 3. Unhexlify
    step3 = binascii.unhexlify(step2)
    
    # 4. XOR dengan kunci
    step4 = bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(step3)])
    
    # 5. Decode base85
    step5 = base64.b85decode(step4)
    
    # 6. Decompress
    step6 = zlib.decompress(step5)
    
    # 7. Loads marshal
    step7 = marshal.loads(step6)
    
    # 8. Eksekusi
    return step7

# Kode terobfuskasi super kompleks
_key = {repr(complex_key)}
_code = "{final_encoded}"

# Jalankan kode
exec(_decode_and_execute(_code, _key))
'''
        return template
    
    def generate_output_filename(self, input_path, suffix):
        path = Path(input_path)
        new_name = f"{path.stem}{suffix}{path.suffix}"
        return str(path.parent / new_name)

    def execute_selected_operation(self):
        """Menjalankan operasi berdasarkan mode yang dipilih"""
        mode = self.mode_var.get()
        
        if mode == "encode":
            # Pilih antara encode atau decode berdasarkan file input
            file_path = self.file_path_var.get()
            if not file_path:
                messagebox.showerror("Error", "Silakan pilih file Python terlebih dahulu.")
                return
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Deteksi apakah file sudah terenkode
            layers = self.detect_encoding_layers(content)
            if layers > 0:
                # File terdeteksi sebagai file yang terenkode, lakukan decode
                self.decode_file()
            else:
                # File tidak terenkode, lakukan encode
                self.encode_file()
        else:
            # Mode obfuscate
            self.obfuscate_file()

# Developed by WONG © 2023-2024
with open('requirements.txt', 'w') as f:
    f.write('sv-ttk==2.5.5')

# Developed by WONG © 2023-2024
if __name__ == "__main__":
    app = ModernGlassApp()
    app.mainloop() 