from django.db import models

from services import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='materials/course/', **NULLABLE, verbose_name='Картинка')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='materials/course/', **NULLABLE, verbose_name='Картинка')
    url = models.URLField(**NULLABLE, verbose_name='Ссылка на видео')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.title} (курс: {self.course})'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
