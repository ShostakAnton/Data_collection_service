from django.contrib import admin
from .models import City, Language, Vacancy


class VacancyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "url", "company"]  # отображение полей на админ-панели

    class Meta:
        model = Vacancy


admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy, VacancyAdmin)
