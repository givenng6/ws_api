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


    booking = {'email': email, 'username': username, 'from': source, 'to': to,'status': 'waiting'}
    ref = db.collection("CampusControl").document(source)
    student_num = email.split('@')[0]
    ref.update({f"students.{student_num}": booking})

    return Response({True})

@api_view(['GET'])
def get_all_residences(request):
     ref = db.collection("CampusControl").document('Original')
     doc = ref.get().to_dict()

     residences = doc['residents']

     return Response(residences)

@api_view(['GET'])
def get_all_campuses(request):

    docs = db.collection('CampusControl').where('campusName', u'!=', 'null').stream()
    campuses = []

    for doc in docs:
        campus = doc.to_dict()
        campuses.append({"campusName": campus['campusName'], "driver": campus['driverName'], "numPlate": campus['numPlate'], "carName": campus['carName']})

    return Response(campuses)





