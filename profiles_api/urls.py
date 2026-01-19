from django.urls import path,include
from profiles_api import views 
from rest_framework.routers import DefaultRouter # Importing DefaultRouter from rest_framework.routers TO HANDLE VIEWSETS why we use it : because viewsets do not handle urls like APIView so we use routers to handle the urls for viewsets

router =DefaultRouter()
# Registering the UserProfileViewSet with the router and the base name 'profile' because we want to access user profile related endpoints using this base name
router.register('hello-viewset',views.HelloViewSet,basename='hello-viewset') # Registering the HelloViewSet with the router
#we dont need to provide basename for UserProfileViewSet because it has queryset attribute defined in the viewset
router.register('profile',views.UserProfileViewSet) # Registering the UserProfileViewSet with the router')
#we dont need to provide basename for UserProfileFeedViewSet because it has queryset attribute defined in the viewset
router.register('feed',views.UserProfileFeedViewSet) # Registering the UserProfileFeedView
urlpatterns = [
    path ('hello-view/',views.HelloWorldView.as_view()),
    path('mjd/',views.Hello.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
]
