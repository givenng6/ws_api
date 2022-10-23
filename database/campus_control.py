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

    doc = db.collection('CampusControl').document(source)
    data = doc.get().to_dict()

    driver = data['driverName']
    carName = data['carName']
    reg = data['numPlate']

    rideInfo = {'status': 'waiting', 'driver': driver, 'reg': reg, 'carName': carName, 'to': to, 'from': source, 'completed': False}

    try:
        ride = db.collection("Rides").document(email)
        ride.update({'status': 'waiting'})
        ride.update({'driver': driver})
        ride.update({'carName': carName})
        ride.update({'reg': reg})
        ride.update({'to': to})
        ride.update({'from': source})
        ride.upadate({'completed': False})
    except:
        ride = db.collection("Rides").document(email).set(rideInfo)
    

    return Response(rideInfo)

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

@api_view(['POST'])
def ride_status(request):
    email = request.data['email']

    status = {}
    try:
        ref = db.collection("Rides").document(email)
        status = ref.get().to_dict()
        print(len(status))
    except:
        status = {"status": "N/A"}

    return Response(status)

@api_view(['POST'])
def cancel_ride(request):
    email = request.data['email']
    source = request.data['from']

    studentNumber = email.split('@', 1)

    route = 'students.'+studentNumber[0]

    try:
        db.collection('Rides').document(email).delete()
        db.collection('CampusControl').document(source).update({
            route: firestore.DELETE_FIELD
        })
        return Response({'isDeleted': True})
    except:
        return Response({'isDeleted': False})