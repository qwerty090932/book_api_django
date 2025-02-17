from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:  # Генерируем QR-код только если он не был сгенерирован ранее
            self.generate_qr_code()

    def generate_qr_code(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.id)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        file_name = f'qr_code_{self.id}.png'
        self.qr_code.save(file_name, File(buffer), save=False)
        self.save()

    def __str__(self):
        return self.title
