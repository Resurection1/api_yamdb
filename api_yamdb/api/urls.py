from django.urls import include, path
from rest_framework import routers

from api.views import (
    CommentViewSet,
    ReviewViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)
from users.views import UserSignupView, TokenView

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)

urlpatterns = [
    path('auth/signup/', UserSignupView.as_view(), name='signup'),
    path('auth/token/', TokenView.as_view(), name='token'),
    path('', include(router_v1.urls)),
]
