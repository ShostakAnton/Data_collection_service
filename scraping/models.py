from django.db import models
import jsonfield
from scraping.utils import from_cyrillic_to_eng

def default_urls():
    return {'work': '', 'rabota': '', 'dou': '', 'djinni': ''}

class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название населенного пункта',
                            unique=True)  # для уникальности данного поля
    slug = models.CharField(max_length=50,
                            blank=True,  # поле может быть пустым
                            unique=True)


    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # переопределение метода save
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
            # super() - ф-ция которая определена в базовам классе моделей
        super().save(*args, **kwargs)  # сохранение


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Язык программирования',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # переопределение метода save
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
            # super() - ф-ция которая определена в базовам классе моделей
        super().save(*args, **kwargs)  # сохранение


class Vacancy(models.Model):

    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город',
                             related_name='vacancies')      # для получения всех связующих с этим полем вакансий, qs = City.objects.all()[0].vacancies.all()
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()        # jsonfield -  для сохранения json полей в sqlite3

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.timestamp)

class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=default_urls)
    
    class Meta:
        unique_together = ('city', 'language')         # указаные параметры уникальные
















