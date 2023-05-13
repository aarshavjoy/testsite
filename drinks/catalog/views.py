from django.http import JsonResponse
from .models import Drink
from .serializers import Drinkserializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import SignupSerializer
from .serializers import DrinkSerializer
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token 
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import(
   HTTP_400_BAD_REQUEST,
   HTTP_200_OK,
   HTTP_404_NOT_FOUND
   
)







# Create your views here.

@api_view(['GET','POST'])
def drink_list(request):

  if request.method=='GET':  
    drinks = Drink.objects.all()
    serializer=Drinkserializer(drinks,many=True)
    return JsonResponse({'drinks':serializer.data}, safe=True)
  

  if request.method=='POST':
     serializer=Drinkserializer(data=request.data)
     if serializer.is_valid():
       serializer.save()
       return Response(serializer.data, status=status.HTTP_201_CREATED)
     



    

@api_view(['GET'])
def search(request):
    # Get the search query from the request's GET parameters
    search_query = request.GET.get('search_query', '')
    drinks = []
    
    if search_query != '':
        # Perform the search query using the model's filter() method
        drinks = Drink.objects.filter(name__icontains=search_query) | Drink.objects.filter(description__icontains=search_query)

    # Serialize the search results using a serializer
    serializer = DrinkSerializer(drinks, many=True)

    # Return the search results in a response
    return Response(serializer.data)






       

@api_view(['GET','PUT','DELETE'])
def drink_details(request,id):
  

  try:
    drink = Drink.objects.get(pk=id)
  except Drink.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method =='GET':
    serializer = Drinkserializer(drink)
    return Response(serializer.data)
  elif request.method =='PUT':
    serializer=Drinkserializer( drink,data=request.data)
    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_404_BAD_REQUEST)
  elif request.method =='DELETE':
    drink.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    try:
        if serializer.is_valid():
            User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name']
            )
            # create a new token

            return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#sample code 
@api_view(['POST'])
def simpleapi(request):
   return Response({"text":'hello aarsha'},status= status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)



