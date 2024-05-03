from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("<str:username>/", views.UserDetailAPIView.as_view(), name="profile"),
]