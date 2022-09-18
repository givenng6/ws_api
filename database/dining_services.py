from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from authentication import firebase_key
from firebase_admin import firestore 
import firebase_admin

db = firebase_admin.firestore.client()

def getTimeAPI():
    """
    get current time from external api
    """
    response = requests.get("http://worldtimeapi.org/api/timezone/Africa/Johannesburg")
    data = response.json()

    datetime = data["datetime"].split("T")
    temp_time = datetime[1].split(".")
    time = temp_time[0]
    
    return time

@api_view(["GET"])
def getTime(request):

    time = getTimeAPI()
    hour = time.split(":")
    meal = "Breakfast"

    if(int(hour[0]) >= 9 and int(hour[0]) < 14):
        meal = "Lunch"
    elif(int(hour[0]) >= 14 and int(hour[0]) < 19):
        meal = "Dinner"


    return Response(meal);

@api_view(["GET"])
def get_dining_halls(request):
    
    dh = []
    # fetch all the list of dinings...
    docs = db.collection('Dining/DiningHalls/DiningHallNames').stream()

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
    