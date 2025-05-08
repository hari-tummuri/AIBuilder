from django.urls import path
from itassist import views

urlpatterns = [
    path('new_conv/', views.create_conversation),
    path('delete_conv/<str:conv_id>/', views.delete_conversation),
    path('get_all_conv/', views.get_all_conversations),
    path("update_conv/<str:conv_id>/", views.update_conversation),
    path("add_message/<str:conv_id>/", views.add_user_message_to_conversation),
    path("conversation/<str:conv_id>/", views.get_conversation_detail_view),
    path("sync/", views.sync_data_sql_server),
    #path for list_files view
    path("list_files/", views.list_files),
    path("download_file/", views.download_file),
]