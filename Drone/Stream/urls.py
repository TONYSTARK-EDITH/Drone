from cv2 import log
from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="login"),
    path("register", register, name="Register"),
    path("login", signin, name="Login"),
    path("home",welcome, name="Home"),
    path('logout', signout, name="Logout"),
    path('add', add_situations, name="Add"),
    path("live", live_feed, name="live_feed")
]