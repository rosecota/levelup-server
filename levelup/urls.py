from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from levelupapi.views import register_user, login_user
from levelupapi.views import GameTypeView, GameView, EventView

router = routers.DefaultRouter(trailing_slash=False)
router.register('gametypes', GameTypeView, 'gametype')
router.register('games', GameView, 'game')
router.register('events', EventView, 'event')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
