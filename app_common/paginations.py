from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 20 #page_size – Har bir sahifada nechta obyekt bo‘lishini belgilaydi
    page_size_query_param = 'page_size' #page_size_query_param – Foydalanuvchi URL orqali sahifa o‘lchamini o‘zgartira oladi
    max_page_size = 50 #max_page_size – Maksimal ruxsat berilgan sahifa hajmi