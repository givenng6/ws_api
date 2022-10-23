import firebase_admin
from rest_framework.decorators import api_view
from rest_framework.response import Response

db = firebase_admin.firestore.client()


@api_view(["GET"])
def get_bus_schedule(request):
    schedule = []
    # fetch all the list of buses...
    docs = db.collection('Buses').stream()

    for doc in docs:
        schedule.append(doc.to_dict())

    return Response(schedule)


@api_view(["POST"])
def follow_bus(request):
    email = request.data['email']
    bus_id = request.data['id']

    ref = db.collection("Users").document(email)
    doc = ref.get()
    user_data = doc.to_dict()['busFollowing']
    bus_following = [bus_id]

    if len(user_data) > 0:
        bus_following.append(user_data[0])

    ref.update({'busFollowing': bus_following})

    """
    Remove the ealiest route...
    # must return the new updated list
    """
    return Response(bus_following)


@api_view(["POST"])
def get_bus_following(request):
    email = request.data['email']

    ref = db.collection("Users").document(email)
    bus_following = []

    try:
        doc = ref.get()
        bus_following = doc.to_dict()['busFollowing']
    except:
        ref.update({'busFollowing': []})

    return Response(bus_following)
