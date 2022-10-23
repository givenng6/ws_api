import email
from requests import session
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication import firebase_key
from firebase_admin import firestore 
import firebase_admin
import uuid

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
    studentName = request.data['studentName']

    if email != '':
        id = str(uuid.uuid4())
        session = date + " " + time
        available = True

        # must set status to pending 
        appointment = {'creator': email, 'studentName': studentName, 'status': 'Pending', 'time': time, 'date': date, 'description': description, 'counsellor': counsellor, 'location': location, 'counsellorName': counsellorName, "id": id}

        if counsellor == '':
            # No counsellor has been selected...
            db.collection('Appointments').document(id).set(appointment)
            response = {'status': available, 'id': id}
            return Response(response)

        doc_ref = db.collection('Users').document(counsellor)
        data = doc_ref.get().to_dict()

        bookings = []
        try:
            bookings = data['bookings']
        except:
            pass

        for meeting in bookings:
            if meeting == session:
                available = False

        if(available):
            db.collection('Appointments').document(id).set(appointment)
            doc_ref.update({'bookings': firestore.ArrayUnion([session])})

        response = {'status': available, 'id': id}
            
        return Response(response)

    return Response({})

    
@api_view(['POST'])
def get_bookings(request):
    email = request.data['email']

    docs = db.collection('Appointments').where('creator', u'==', email).stream()
    appointments = []

    for doc in docs:
        appointments.append(doc.to_dict())

    return Response(appointments)
    

@api_view(['GET'])
def get_counsellors(request):
    docs = db.collection('Users').where('department', u'==', 'CCDU').stream()

    counsellors = []

    for doc in docs:
        counsellor = {'email': doc.to_dict()['email'], 'username': doc.to_dict()['username']}
        counsellors.append(counsellor)

    return Response(counsellors)
