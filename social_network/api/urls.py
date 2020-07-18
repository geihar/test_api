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
    path("upvotes/", views.AddLike.as_view()),
]
#
#
