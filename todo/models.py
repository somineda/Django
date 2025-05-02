from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from pathlib import Path

class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # 어떤 유저가 만든건지
    completed_image = models.ImageField(upload_to='completed/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True, default='default/thumb.jpg')

    def save(self, *args, **kwargs):
        if self.completed_image:
            img = Image.open(self.completed_image)
            img.thumbnail((200, 200))

            thumb_io = BytesIO()
            filename = Path(self.completed_image.name).stem
            ext = Path(self.completed_image.name).suffix.lower()

            file_type = 'JPEG' if ext in ['.jpg', '.jpeg'] else 'PNG'
            new_filename = f"{filename}_thumb{ext}"

            img.save(thumb_io, file_type)
            self.thumbnail.save(new_filename, ContentFile(thumb_io.getvalue()), save=False)
            thumb_io.close()

        super().save(*args, **kwargs)


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.message[:20]}'
