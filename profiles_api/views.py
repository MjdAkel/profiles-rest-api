from rest_framework.views import APIView # Importing APIView from rest_framework
from rest_framework.response import Response # Importing Response from rest_framework
from rest_framework import status # Importing status from rest_framework
from profiles_api import serializers
from rest_framework import viewsets
from profiles_api import models
from rest_framework.permissions import IsAuthenticated
# we use it for users to auth themselfs with our api it works by generating
# a random token when the user logs in  and then the user includes that token in the header of future requests to authenticate themselves
from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions
from rest_framework import filters
from profiles_api.permissions import UpdateOwnStatus
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
class HelloWorldView(APIView):
    """A simple APIView that returns a hello world message."""
    serializer_class = serializers.HelloSerializer

    def get(self,request,format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]
    
        return Response ({'messege' : 'Hello!', 'an_api_view': an_apiview})
    def post(self,request): # Handling POST requests
        serializer = self.serializer_class(data=request.data) # Initializing the serializer with request data AND data is used to pass data into serializer for validation
         # Checking if the serializer data is valid
        if serializer.is_valid():
            name = serializer.validated_data.get('name') # Retrieving the 'name' field from validated data
            message = f'Hello{name}' # Creating a message using the name f is for formatted string literals
            return Response({'message': message}) # Returning the message in the response
        else :
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) # Returning errors if the serializer is not valid with a 400 Bad Request status
    def put (self,request,pk=None): # Handling PUT requests 
        """to update an object """
        """pk is the id of the object that we wanna update """
        return Response({'method':'PUT'}) # Returning a response indicating the method used
    def patch (self,request, pk=None): # Handling PATCH requests patch is for partial update and put is for full update
        """to do an update but only the fields that we prvided in the request """
        return Response({'method': 'PATCH'}) # Returning a response indicating the method used
    def delete(self , request ,pk=None): # Handling DELETE requests
        """delete an object """
        return Response({'method':'DELETE'})    # Returning a response indicating the method used






class HelloViewSet(viewsets.ViewSet): # A simple ViewSet that returns a hello message.
    serializer_class = serializers.HelloSerializer
    def list(self , request ): # Handling GET requests for listing objects
        """return hello message"""
        a_viewset=[ # List of features of a ViewSet
             'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]
        return Response ({'message':'hello','a_viewset': a_viewset})
    
    
    def create(self , request): # Handling POST requests for creating objects
        serializer = self.serializer_class(data=request.data) # Initializing the serializer with request data
        if serializer.is_valid(): # Checking if the serializer data is valid
            name = serializer.validated_data.get('name') # Retrieving the 'name' field from validated data
            message = f'Hello {name}' # Creating a message using the name
            return Response({'message': message})
        else:
            return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST )
        
    def retrieve(self,request,pk=None): # Handling GET requests for retrieving a single object
        return Response({'http_method' : 'GET'})
    def update (self,requerst ,pk=None ):  # Handling PUT requests for updating objects
        """handle updating an object """
        return Response({'http_method':'PUT'})
    def partial_update(self,request,pk=None): # Handling PATCH requests for partially updating objects
        """handle updating part of an object """
        return Response({'http_method':'PATCH'})
    def destroy(self,request,pk=None): # Handling DELETE requests for deleting objects
        """handle removing an object """
        return Response({'http_method':'DELETE'})
class Hello (APIView):
        def get(self,request,format=None): 
            return Response ({'messege':'hello mjd'})


# User Profile ViewSet we use ModelViewSet which provides default implementations for CRUD operations
class UserProfileViewSet(viewsets.ModelViewSet): 
    """ Handle creating and updating profiles """
    serializer_class = serializers.UserProfileSerializer  # specify the serializer class to be used for this viewset
    queryset = models.UserProfile.objects.all() # specify the queryset to be used for this viewset which retrieves all user profile objects from the database
    authentication_classes = (TokenAuthentication,) # specify the authentication classes to be used for this viewset
    permission_classes = (permissions.UpdateOwnProfile,)    # specify the permission classes to be used for this viewset and the , in the end is for  element tupple
    filter_backends = (filters.SearchFilter,) # Enable search functionality
    search_fields = ('name', 'email', 'username',) # Specify fields to be searched
    
    
    



class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
