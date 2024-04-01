from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.MangaCreateView.as_view()),
    path('index/', views.IndexListView.as_view()),
    path('detail/<int:pk>/', views.MangaDetailView.as_view()),
    path('bookmarks/', views.BookmarksView.as_view()),
    path('popular/', views.PopularListView.as_view()),
    path('bestsellers/', views.BestSellerListView.as_view()),
    path('', views.MangaListView.as_view())
]
