from django.urls import path

from .views import index, detail

app_name = "nfctags"

urlpatterns = [
    path('', index, name='index'),
    path('<int:nfc_tag_id>/', detail, name='detail')
]