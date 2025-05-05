from django.db import models
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from pathlib import Path
from bs4 import BeautifulSoup


class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    completed_image = models.ImageField(
        upload_to='completed/', null=True, blank=True
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/', null=True, blank=True, default='default/thumb.jpg'
    )

    def __str__(self):
        return f'{self.title} ({self.user.username if self.user else "Unknown"})'

    def save(self, *args, **kwargs):
        # 저장 전: 썸네일 생성
        if self.completed_image:
            image = Image.open(self.completed_image)
            image.thumbnail((100, 100), Image.ANTIALIAS)

            image_path = Path(self.completed_image.name)
            ext = image_path.suffix.lower()
            filename = image_path.stem

            thumbnail_filename = f"{filename}_thumbnail{ext}"

            if ext in ['.jpg', '.jpeg']:
                file_type = 'JPEG'
            elif ext == '.png':
                file_type = 'PNG'
            elif ext == '.gif':
                file_type = 'GIF'
            else:
                return super().save(*args, **kwargs)

            temp_thumb = BytesIO()
            image.save(temp_thumb, format=file_type)
            temp_thumb.seek(0)

            self.thumbnail.save(thumbnail_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()

        return super().save(*args, **kwargs)

    @property
    def description_first_image(self):
        """description 필드에서 첫 번째 <img> 태그의 src를 반환"""
        soup = BeautifulSoup(self.description, 'html.parser')
        img = soup.find('img')
        return img['src'] if img and img.has_attr('src') else None


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.message[:20]}'
