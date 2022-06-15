from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, Course, Lesson, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonTagInLine(admin.StackedInline):
    model = Lesson.tags.through


class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/main.css',)
        }

    form = LessonForm
    list_display = ["id", "subject", "create_date", "active", "course"]
    search_fields = ["subject", "create_date", "course__subject"]
    list_filter = ["subject", "course__subject"]
    readonly_fields = ["avatar"]
    inlines = (LessonTagInLine,)

    def avatar(self, lesson):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width='120px' />".format(img_url=lesson.image.name,
                                                                                            alt=lesson.subject))


class LessonInLine(admin.StackedInline):
    model = Lesson
    pk_name = 'courses'


class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInLine,)

# Register your models here.
# admin gốc của django
admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)

