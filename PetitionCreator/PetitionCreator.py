from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
import sys


def get_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def turkish_upper(text):
    tr_map = {
        'ı': 'I',
        'i': 'İ',
        'ğ': 'Ğ',
        'ü': 'Ü',
        'ş': 'Ş',
        'ö': 'Ö',
        'ç': 'Ç',
    }
    result = ""
    for char in text:
        if char in tr_map:
            result += tr_map[char]
        else:
            result += char.upper()
    return result


def get_downloads_folder():
    if os.name == 'nt':
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
                downloads = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
                return downloads
        except Exception:
            pass
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        return os.path.join(os.path.expanduser("~"), "Downloads")


def create_petition_pdf(data):
    pdfmetrics.registerFont(TTFont("Times-Roman", get_resource_path("times.ttf")))
    pdfmetrics.registerFont(TTFont("Times-Bold", get_resource_path("timesbd.ttf")))
    
    downloads_folder = get_downloads_folder()
    
    dosya_adi = data["dosya_adi"]
    if dosya_adi.lower().endswith(".pdf"):
        dosya_adi = dosya_adi[:-4]
    
    output_path = os.path.join(downloads_folder, f"{dosya_adi}.pdf")
    
    counter = 1
    base_path = output_path
    while os.path.exists(output_path):
        output_path = base_path.replace(".pdf", f"_{counter}.pdf")
        counter += 1
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=65,
        leftMargin=65,
        topMargin=60,
        bottomMargin=50
    )

    content = []

    title_style = ParagraphStyle(
        name="Title",
        fontName="Times-Bold",
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
    )

    text_style = ParagraphStyle(
        name="Text",
        fontName="Times-Roman",
        fontSize=16,
        leading=24,
        alignment=TA_LEFT,
    )

    indent_style = ParagraphStyle(
        name="IndentText",
        parent=text_style,
        firstLineIndent=15
    )

    content.append(Paragraph("T.C.", title_style))
    content.append(Paragraph(turkish_upper(data["universite"]), title_style))
    content.append(Paragraph(turkish_upper(data["fakulte"]), title_style))
    content.append(Paragraph(turkish_upper(data["birim"]), title_style))

    content.append(Spacer(1, 35))

    content.append(Paragraph(
        f"<b>Konu:</b> {data['sinav_turu']} Sınav Sonucuna İtiraz Hakkında",
        text_style
    ))

    content.append(Spacer(1, 25))

    content.append(Paragraph(
        f"Ben {data['ad_soyad']}, {data['bolum']} bölümü {data['ogrenci_no']} numaralı öğrencisiyim. "
        f"{data['akademik_yil']} akademik yılı {data['donem']} dönemi kapsamında yapılan "
        f"{data['ders']} dersinin {data['sinav_turu']} sınavına katıldım.",
        indent_style
    ))

    content.append(Spacer(1, 25))

    content.append(Paragraph(
        f"İlgili dersin {data['sinav_turu']} sınavı sonucunda almış olduğum notun, sınav performansımı "
        f"tam olarak yansıtmadığını düşünmekteyim. Sınav kağıdımın değerlendirilmesi sırasında maddi "
        f"bir hata yapılmış olabileceği kanaatindeyim. Bu nedenle, sınav kağıdımın yeniden incelenmesini "
        f"ve maddi hata yönünden kontrol edilmesini talep ediyorum.", 
        indent_style
    ))

    content.append(Spacer(1, 25))

    content.append(Paragraph("Gereğini bilgilerinize arz ederim.", indent_style))

    content.append(Spacer(1, 35))

    content.append(Paragraph(f"Tarih: {data['tarih']}", text_style))
    content.append(Paragraph(f"Ad Soyad: {data['ad_soyad']}", text_style))
    content.append(Paragraph(f"Öğrenci No: {data['ogrenci_no']}", text_style))
    content.append(Paragraph(f"Bölüm: {data['bolum']}", text_style))
    content.append(Paragraph("İmza:", text_style))

    doc.build(content)
    
    return output_path


def PetitionCreator():
    sample_data = {
        "universite": "Örnek Üniversitesi",
        "fakulte": "Mühendislik Fakültesi",
        "birim": "Dekanlığına",
        "ad_soyad": "Örnek İsim",
        "ogrenci_no": "123456789",
        "bolum": "Bilgisayar Mühendisliği",
        "ders": "Programlama",
        "akademik_yil": "2024-2025",
        "donem": "Güz",
        "sinav_turu": "Vize",
        "tarih": "01.01.2025",
        "dosya_adi": "ornek_dilekce"
    }
    
    return create_petition_pdf(sample_data)


if __name__ == "__main__":
    PetitionCreator()