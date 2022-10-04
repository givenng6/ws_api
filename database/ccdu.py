import email
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication import firebase_key
from firebase_admin import firestore 
import firebase_admin

db = firebase_admin.firestore.client()


@api_view(['POST'])
def book_session(request):
    email = request.data['email']
    time =  request.data['time']
    date =  request.data['date']
    description =  request.data['description']
    counsellor =  request.data['counsellor']
    counsellorName =  request.data['counsellorName']
    location =  request.data['location']

    # must set status to pending 
    appointment = {'creator': email, 'status': 'Pending', 'time': time, 'date': date, 'description': description, 'counsellor': counsellor, 'location': location, 'counsellorName': counsellorName}
    db.collection('Appointments').add(appointment)

    return Response({})

@api_view(['POST'])
def get_bookings(request):
    email = request.data['email']

    docs = db.collection('Appointments').where('creator', u'==', email).stream()
    appointments = []

    for doc in docs:
        appointments.append(doc.to_dict())

    return Response(appointments)