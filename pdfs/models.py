from django.db import models
from django.conf import settings
from PIL import Image
from fpdf import FPDF
import os

def reducir_peso_imagen(imagen_path, max_peso_mb):
    imagen = Image.open(imagen_path)
    calidad = 85  # Puedes ajustar esto según tus necesidades
    imagen.save(imagen_path, quality=calidad)

    peso_actual_mb = os.path.getsize(imagen_path) / (600 * 600)

    if peso_actual_mb > max_peso_mb:
        reducir_factor = max_peso_mb / peso_actual_mb
        nueva_calidad = int(calidad * reducir_factor)

        imagen = Image.open(imagen_path)
        imagen.save(imagen_path, quality=nueva_calidad)

def crear_pdf_con_imagenes(carpeta_entrada, pdf_salida):
    pdf = FPDF()
    imagenes_para_eliminar = []

    for root, _, files in os.walk(carpeta_entrada):
        for archivo in files:
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                imagen_path = os.path.join(root, archivo)
                reducir_peso_imagen(imagen_path, 2)  # Ajusta el límite de peso como desees
                pdf.add_page()
                pdf.image(imagen_path, x=10, y=10, w=190)
                imagenes_para_eliminar.append(imagen_path)

    pdf.output(pdf_salida)

    # Eliminar las imágenes después de crear el PDF
    for imagen_path in imagenes_para_eliminar:
        os.remove(imagen_path)

class ConvertPDF(models.Model):
    archivo1 = models.ImageField(upload_to='temp')
    archivo2 = models.ImageField(upload_to='temp', null=True, blank=True)
    archivo3 = models.ImageField(upload_to='temp', null=True, blank=True)
    archivo4 = models.ImageField(upload_to='temp', null=True, blank=True)
    archivo5 = models.ImageField(upload_to='temp', null=True, blank=True)
    archivo6 = models.ImageField(upload_to='temp', null=True, blank=True)
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        carpeta_entrada = os.path.join(settings.MEDIA_ROOT, "temp")  # Ruta completa al directorio temp en tus medios
        pdf_nombre = f"resultado_{self.pk}.pdf"
        pdf_salida = os.path.join(settings.MEDIA_ROOT, "pdf", pdf_nombre)  # Ruta completa al archivo resultado.pdf en tus medios

        crear_pdf_con_imagenes(carpeta_entrada, pdf_salida)
        self.pdf.name = os.path.join("pdf", pdf_nombre)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Eliminar el archivo PDF asociado
        if self.pdf:
            pdf_path = os.path.join(settings.MEDIA_ROOT, self.pdf.name)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        # Llamar al método delete del modelo base
        super().delete(*args, **kwargs)
