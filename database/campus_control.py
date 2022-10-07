import email
from requests import session
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication import firebase_key
from firebase_admin import firestore 
import firebase_admin

db = firebase_admin.firestore.client()

@api_view(['POST'])
def request_ride(request):
    email = request.data['email']
    username = request.data['username']
    source = request.data['from']
    to = request.data['to']


    booking = {'email': email, 'username': username, 'from': source, 'to': to}
    ref = db.collection("CampusControl").document(source)
    ref.update({'students': firestore.ArrayUnion([booking])})

    return Response({})







