
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('adduser', views.addUser, name='adduser'),
    path('changepassword', views.changePassword, name='changepassword'),
    path('uploadfile', views.uploadFile, name='uploadfile'),
    path('viewfile', views.viewFile, name='viewfile'),
    path('viewuser', views.viewUser, name='viewuser'),
    path('viewcategory/<category>', views.viewCategoryFile, name='viewcategory'),
    path('edituser/<user_id>', views.editUser, name='edituser'),
    path('openpdf/<file_name>', views.openPDF, name='openpdf'),
    path('openimage/<file_name>', views.openImage, name='openimage'),
    path('opendoc/<file_name>', views.openDoc, name='opendoc'),
    path('downloadfile/<file_name>', views.downloadFile, name='downloadfile'),

]

