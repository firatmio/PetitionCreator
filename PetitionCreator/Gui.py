import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import os
import sys
import platform
from PetitionCreator import create_petition_pdf


def get_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


class PetitionCreatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Sınav İtiraz Dilekçesi Oluşturucu")
        self.geometry("520x680")
        self.minsize(480, 640)
        
        self._set_app_icon()
        
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.main_frame.configure(fg_color=("gray90", "gray14"))
        
        self._create_form_fields()
        
        self.create_button = ctk.CTkButton(
            self.main_frame,
            text="Dilekçe Oluştur",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=8,
            command=self.create_petition
        )
        self.create_button.pack(pady=(25, 15), fill="x", padx=15)
    
    def _set_app_icon(self):
        current_os = platform.system()
        
        try:
            if current_os == "Windows":
                icon_path = get_resource_path(os.path.join("icons", "icon.ico"))
                if os.path.exists(icon_path):
                    self.iconbitmap(icon_path)
            elif current_os == "Darwin":
                icon_path = get_resource_path(os.path.join("icons", "icon.png"))
                if os.path.exists(icon_path):
                    from PIL import Image, ImageTk
                    img = Image.open(icon_path)
                    photo = ImageTk.PhotoImage(img)
                    self.iconphoto(True, photo)
                    self._icon_photo = photo
            else:
                icon_path = get_resource_path(os.path.join("icons", "icon.png"))
                if os.path.exists(icon_path):
                    from PIL import Image, ImageTk
                    img = Image.open(icon_path)
                    photo = ImageTk.PhotoImage(img)
                    self.iconphoto(True, photo)
                    self._icon_photo = photo
        except Exception:
            pass
    
    def _create_form_fields(self):
        self.universite_entry = self._create_entry_field("Üniversite Adı:", "Örnek: Trabzon Üniversitesi")
        self.fakulte_entry = self._create_entry_field("Fakülte / Yüksekokul Adı:", "Örnek: Bilgisayar ve Bilişim Bilimleri Fakültesi")
        
        self.birim_label = ctk.CTkLabel(
            self.main_frame,
            text="Birim Türü:",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.birim_label.pack(anchor="w", pady=(10, 5), padx=20)
        
        self.birim_var = ctk.StringVar(value="Dekanlığına")
        self.birim_segmented = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["Dekanlığına", "Müdürlüğüne"],
            variable=self.birim_var,
            font=ctk.CTkFont(size=12)
        )
        self.birim_segmented.pack(fill="x", pady=(0, 5), padx=15)
        
        self.ad_soyad_entry = self._create_entry_field("Ad Soyad:", "Örnek: Arda BALCI")
        self.ogrenci_no_entry = self._create_entry_field("Öğrenci Numarası:", "Örnek: 123456789")
        self.bolum_entry = self._create_entry_field("Bölüm Adı:", "Örnek: Bilgisayar Mühendisliği")
        
        self.ders_entry = self._create_entry_field("Ders Adı:", "Örnek: Veri Yapıları")
        self.akademik_yil_entry = self._create_entry_field("Akademik Yıl:", "Örnek: 2025-2026")
        
        self.donem_label = ctk.CTkLabel(
            self.main_frame,
            text="Dönem:",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.donem_label.pack(anchor="w", pady=(10, 5), padx=20)
        
        self.donem_var = ctk.StringVar(value="Güz")
        self.donem_segmented = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["Güz", "Bahar"],
            variable=self.donem_var,
            font=ctk.CTkFont(size=12)
        )
        self.donem_segmented.pack(fill="x", pady=(0, 5), padx=15)
        
        self.sinav_turu_label = ctk.CTkLabel(
            self.main_frame,
            text="Sınav Türü:",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.sinav_turu_label.pack(anchor="w", pady=(10, 5), padx=20)
        
        self.sinav_turu_var = ctk.StringVar(value="Vize")
        self.sinav_turu_segmented = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["Vize", "Final", "Bütünleme"],
            variable=self.sinav_turu_var,
            font=ctk.CTkFont(size=12)
        )
        self.sinav_turu_segmented.pack(fill="x", pady=(0, 5), padx=15)
        
        today = datetime.now().strftime("%d.%m.%Y")
        self.tarih_entry = self._create_entry_field("Tarih (GG.AA.YYYY):", today)
        self.tarih_entry.delete(0, "end")
        self.tarih_entry.insert(0, today)
        
        self.dosya_adi_entry = self._create_entry_field("Dosya Adı:", "Örnek: sinav_itiraz_dilekcesi")
    
    def _create_entry_field(self, label_text, placeholder):
        label = ctk.CTkLabel(
            self.main_frame,
            text=label_text,
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        label.pack(anchor="w", pady=(10, 5), padx=20)
        
        entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text=placeholder,
            height=38,
            font=ctk.CTkFont(size=12),
            corner_radius=6
        )
        entry.pack(fill="x", pady=(0, 5), padx=15)
        
        return entry
    
    def validate_fields(self):
        required_fields = {
            "Üniversite Adı": self.universite_entry.get(),
            "Fakülte/Yüksekokul Adı": self.fakulte_entry.get(),
            "Ad Soyad": self.ad_soyad_entry.get(),
            "Öğrenci Numarası": self.ogrenci_no_entry.get(),
            "Bölüm Adı": self.bolum_entry.get(),
            "Ders Adı": self.ders_entry.get(),
            "Akademik Yıl": self.akademik_yil_entry.get(),
            "Tarih": self.tarih_entry.get(),
            "Dosya Adı": self.dosya_adi_entry.get()
        }
        
        empty_fields = [name for name, value in required_fields.items() if not value.strip()]
        
        if empty_fields:
            messagebox.showerror(
                "Eksik Bilgi",
                "Lütfen şu alanları doldurun:\n\n- " + "\n- ".join(empty_fields)
            )
            return False
        
        return True
    
    def create_petition(self):
        if not self.validate_fields():
            return
        
        try:
            data = {
                "universite": self.universite_entry.get().strip(),
                "fakulte": self.fakulte_entry.get().strip(),
                "birim": self.birim_var.get(),
                "ad_soyad": self.ad_soyad_entry.get().strip(),
                "ogrenci_no": self.ogrenci_no_entry.get().strip(),
                "bolum": self.bolum_entry.get().strip(),
                "ders": self.ders_entry.get().strip(),
                "akademik_yil": self.akademik_yil_entry.get().strip(),
                "donem": self.donem_var.get(),
                "sinav_turu": self.sinav_turu_var.get(),
                "tarih": self.tarih_entry.get().strip(),
                "dosya_adi": self.dosya_adi_entry.get().strip()
            }
            
            output_path = create_petition_pdf(data)
            
            messagebox.showinfo(
                "Başarılı",
                f"Dilekçeniz başarıyla oluşturuldu!\n\nKonum: {output_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dilekçe oluşturulurken bir hata oluştu:\n\n{str(e)}")


if __name__ == "__main__":
    app = PetitionCreatorApp()
    app.mainloop()
