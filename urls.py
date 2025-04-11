from django.urls import path
from .views import user_list, user_create, user_update, user_delete, export_users_to_excel, export_users_to_pdf
from django.urls import path
from .views import send_email_with_attachment
urlpatterns = [
    path('users/', user_list, name='user_list'),
    path('create/', user_create, name='user_create'),
    path('edit/<int:id>/', user_update, name='user_update'),
    path('delete/<int:id>/', user_delete, name='user_delete'),
    path('export/excel/', export_users_to_excel, name='export_excel'),
    path('export/pdf/', export_users_to_pdf, name='export_pdf'),
    path('send-email/', send_email_with_attachment, name='send_email'),
]