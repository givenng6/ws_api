from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication import firebase_key
from firebase_admin import firestore 
import firebase_admin

db = firebase_admin.firestore.client()

@api_view(["GET"])
def get_dining_halls(request):
    
    dh = []
    # fetch all the list of dinings...
    docs = db.collection('Dining').stream()

    for doc in docs:
        dh.append(doc.to_dict())

    return Response(dh)

@api_view(["POST"])
def follow_dh(request):
    email = request.data['email']
    dh_id = request.data['id']

    ref = db.collection("Users").document(email)
    dh_following = ""

    dh_following = dh_id

    ref.update({'dhFollowing': dh_following})

    return Response({"id": dh_following})

@api_view(["POST"])
def get_dh_following(request):
    email = request.data['email']

    ref = db.collection("Users").document(email)
    dh_following = ""

    try:
        doc = ref.get()
        dh_following = doc.to_dict()['dhFollowing']
    except:
        ref.update({'dhFollowing': ""})

    return Response(dh_following)
    