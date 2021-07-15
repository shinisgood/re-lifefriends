from django.urls import path 

from reviews.views import ReviewView

urlpatterns = [
    path('/<int:product_id>', ReviewView.as_view()),
]
