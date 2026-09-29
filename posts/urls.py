from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostListCreate.as_view(), name="list_all_posts"),
    path(
        "<int:pk>",
        views.PostRetrieveUpdateDeleteView.as_view(),
        name="details_modify_delete_post",
    ),
    path("user/", views.get_posts_for_current_user, name="current_user"),
    # path("<int:post_id>",views.PostRetrieveUpdateDeleteView.as_view(),name="details_modify_delete_post"),
    # path("",views.get_posts,name="list_posts"),
    # path("create/",views.create_posts,name="create_post"),
    # path("<int:post_id>",views.post_detail_modify_delete,name="post_details_modify"),
]
