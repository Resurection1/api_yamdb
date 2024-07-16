from rest_framework import routers

from django.urls import include, path

from api.views import (
    CommentViewSet,
    ReviewViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    # token_post,
    # signup_post,
)

app_name = 'api'

router_v1 = routers.DefaultRouter()
# router_v1.register('users', UserViewSet)
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
    # path('v1/auth/token', token_post),
    # path('v1/auth/signup', signup_post),
    path('v1/', include(router_v1.urls)),
]
