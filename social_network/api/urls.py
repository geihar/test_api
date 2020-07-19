from django.urls import path

from . import views

urlpatterns = [
    path("posts/", views.PostViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "posts/<int:pk>/",
        views.PostViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path("like/", views.AddLike.as_view()),
    path("signup/", views.UserCreate.as_view()),
    path("user/<int:pk>/", views.UserLastActivity.as_view()),
]
#
#
