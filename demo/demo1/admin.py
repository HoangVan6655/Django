from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
#thêm các models
from .models import Category, Course, Lesson, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path

#kế thừa lại modelsform
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget) #content dc sử dụng bộ công cụ ckeditor

    class Meta:
        model = Lesson
        fields = '__all__' #các trường sẽ tương tác

#chỉ định models trung gian tag phải dùng through
class LessonTagInLine(admin.StackedInline):
    model = Lesson.tags.through

#custom admin kế thừa lại modeladmin có sẵn của django
class LessonAdmin(admin.ModelAdmin):
    #thêm css
    class Media:
        css = {
            'all': ('/static/css/main.css',)
        }

    form = LessonForm
    #thuộc tính quy định các trường sẽ hiển thị
    list_display = ["id", "subject", "create_date", "active", "course"]
    #thao tác tìm kiếm - quy định tìm theo những thứ mình muốn - giao diện tìm kiếm mặc định
    search_fields = ["subject", "create_date", "course__subject"]
    #thao tác lọc các chủ đề (tự làm khá là cực - django đã tích hợp sẵn)
    list_filter = ["subject", "course__subject"]
    #trường hiển thị ảnh khi nhấp vào 1 khoá học
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

#tạo ra hàm adminsite kế thừa lại từ admin
class CourseAppAdminSite(admin.AdminSite):
    #tuỳ chỉnh header
    site_header = 'He Thong Quan Ly Khoa Hoc'

    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()

    def course_stats(self, request):
        #đếm có bao nhiêu khoá học
        course_count = Course.objects.count()
        #đếm 1 khoá học có bao nhiêu bài học
        stats = Course.objects.annotate(lesson_count=Count('lessons')).values("id", "subject", "lesson_count")

        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': course_count,
            'stats': stats
        })

admin_site = CourseAppAdminSite('course')

# Register your models here.
# admin gốc của django
# admin.site.register(Category)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Lesson, LessonAdmin)


# admin site
admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
