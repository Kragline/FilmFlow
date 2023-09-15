from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),

    path('user/<str:username>', ProfilePageView.as_view(), name='profile_page'),
    path('user/<str:username>/update/', update_user_view, name='update_user'),
    path('user/<str:username>/delete/', UserDeleteView.as_view(), name='delete_user'),

    path('user/<int:user_id>/change-profile-pic/', ChangeProfilePicView.as_view(), name='change_profile_pic')
]
