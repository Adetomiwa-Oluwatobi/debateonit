# rooms/urls.py
from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('join-room/', views.join_room, name='join_room'),
    path('create/', views.room_create, name='room_create'),
    path('room/<int:room_id>/', views.debate_room, name='debate_room'),
    path('judge/<int:room_id>/', views.judge_room, name='judge_room'),
    path('results/<int:room_id>/', views.debate_results, name='debate_results'),
   
    path('resources/download/<str:resource_id>/', views.download_resource, name='download_resource'),
    path('articles/view/<str:article_id>/', views.view_article, name='view_article'),
    path('tutorial/', views.TutorialListView.as_view(), name='tutorial_list'),
    path('tutorial/<slug:tutorial_slug>/', views.TutorialDetailView.as_view(), name='tutorial_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)