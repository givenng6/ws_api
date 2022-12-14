import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication import firebase_key
from firebase_admin import firestore 
import firebase_admin

db = firebase_admin.firestore.client()

@api_view(['GET'])
def get_events(request):
    docs = db.collection('Events').stream()
    response = []

    for doc in docs:
        response.append(doc.to_dict())
    
    return Response(response)

@api_view(['POST'])
def add_like(request):
    email = request.data['email']
    id = request.data['id']

    ref = db.collection("Events").document(id)

    ref.update({'likes': firestore.ArrayUnion([email])})

    return Response({})



