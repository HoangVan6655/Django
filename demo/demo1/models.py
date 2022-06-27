from django.contrib.auth.models import AbstractUser
#lớp chứng thực user có bộ user chứng thực sẵn
from django.db import models
#import ckeditor
from ckeditor.fields import RichTextField


class User(AbstractUser):
    # tạo class user kế thừa abstractuser
    avatar = models.ImageField(upload_to='upload/%Y/%m')
    #để sử dụng image field phải cài thêm thư viện pillow: pip install pillow


class Category(models.Model):
    # danh mục - phương thức kế thừa của python - mặc định sẽ lấy tên app_tên class model
    name = models.CharField(max_length=100, null=False, unique=True)
    # không được not null, tên là duy nhất không được trùng nhau

    def __str__(self):
        return self.name

class ItemBase(models.Model):
    class Meta:
        abstract = True

    subject = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    # ngày tạo khoá học - khi tạo một khoá học tự động lấy thời điểm hiện tại gán vô biến date
    create_date = models.DateTimeField(auto_now_add=True)
    # ngày update khoá học - chỉ cần có cập nhật thì lấy thời điểm cập nhật gán vô
    update_date = models.DateTimeField(auto_now=True)
    # trường active có nghĩa là xoá, khi xoá chỉ cần tắt trường này đi thôi - khi được tạo ra lúc nào cũng là đang bật
    active = models.BooleanField(default=True)

    #phương thức in ra văn bản
    def __str__(self):
        return self.subject

class Course(ItemBase): #models khoá học
    class Meta:
        # trong danh mục không trùng tên khoá học
        unique_together = ('subject', 'category')
        ordering = ["-id"] #tự động sắp xếp
        #ordering: chỉ định các trường dùng sắp xếp khi truy vấn dữ liệu. Mặc định là sắp xếp tăng, nếu thêm dấu “-” trước tên trường là sắp xếp giảm.

    description = models.TextField(null=True, blank=True)
    # khoá ngoại yêu cầu thêm cái on_delete để khi th categor bị xoá thì xử lý các khoá học ra sao
    # có nhiều giải pháp trong trường hợp xoá 1 category: cascade xoá luôn cả các khoá học, set_null khi xoá sẽ gán các biến trong khoá học là null
    category = models.ForeignKey(Category, on_delete= models.SET_NULL, null=True)

class Lesson(ItemBase):
    class Meta:
        unique_together = ('subject', 'course') #trong khoá học không trùng tên bài học
        # db_table = '...' phương thức đổi tên bảng

    # content = models.TextField()
    content = RichTextField()
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE) #còn 1 thuộc tính là protect là kh thể xoá 1 khoá học có bài học thì kh thể xoá bài học đó
    #khai báo 1 bài học có nhiều tag
    tags = models.ManyToManyField('Tag', blank=True, null=True) #được phép rỗng được phép null
    #nếu Tag để không thì buộc cái models Tag phải được tạo bên trên trước
    #nếu models Tag dc tạo đằng sau thì phải bỏ trong dấu nháy đơn 'Tag'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name