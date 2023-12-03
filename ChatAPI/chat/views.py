from django.shortcuts import redirect, reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import MyUser as User
from .models import Conversation, Room
from .serializers import ConversationListSerializer, ConversationSerializer,RoomSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
def start_convo(request):
    data = request.data
    username = data.get('username', None) 
    if not username:
        return Response({'message': 'Username is required for starting a conversation'}, status=400)

    try:
        participant = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a nonexistent user'}, status=404)

    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))

    if conversation.exists():
        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:
        conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
        return Response(ConversationSerializer(instance=conversation).data)

@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'}, status=404)
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)

@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) | Q(receiver=request.user))
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_room(request):
    room_name = request.data.get('name')

    if not room_name:
        return Response({'message': 'Room name is required'}, status=400)

    room = Room.objects.create(name=room_name)
    room.join(request.user)

    serializer = RoomSerializer(instance=room)
    return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    serializer = RoomSerializer(instance=room)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.join(request.user)
    serializer = RoomSerializer(instance=room)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.leave(request.user)
    serializer = RoomSerializer(instance=room)
    return Response(serializer.data)


