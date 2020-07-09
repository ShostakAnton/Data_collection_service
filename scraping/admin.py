from django.contrib import admin
from .models import City, Language, Vacancy, Error, Url


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "url", "company"]  # отображение полей на админ-панели

    class Meta:
        model = Vacancy


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ["city", "language"]  # отображение полей на админ-панели

    class Meta:
        model = Url


admin.site.register(City)
admin.site.register(Language)
admin.site.register(Error)

