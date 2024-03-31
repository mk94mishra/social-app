from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from django.contrib.auth import get_user_model
from django.core.cache import cache



class FriendRequestViewCreate(CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def create(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user')
        to_user = get_user_model().objects.get(pk=to_user_id)

        if from_user.id == to_user_id:
            return Response({'message': 'You cannot send yourself!'}, status=status.HTTP_400_BAD_REQUEST)

        # Rate limiting for friend requests (using cache)
        cache_key = f"friend_request_from_{from_user.id}"
        request_count = cache.get(cache_key, 0)
        if request_count >= 3:
            return Response({'message': 'Too many requests in a short time'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        cache.set(cache_key, request_count + 1, timeout=60)  # Increment and expire after 1 minute

        # Check for existing pending request
        existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='PENDING').first()

        if existing_request:
            return Response({'message': 'Request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for if received request from to_user
        existing_request = FriendRequest.objects.filter(from_user=to_user, to_user=from_user, status='PENDING').first()

        if existing_request:
            return Response({'message': 'You already received a Request'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(from_user=from_user, to_user=to_user)

        return Response({'message': f'Request sent!', 'user':serializer.data['to_user']}, status=status.HTTP_201_CREATED)


class FriendRequestViewUpdate(UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 
    def perform_update(self, serializer):
        if self.request.user.id == serializer.instance.from_user.id or self.request.user.id != serializer.instance.to_user.id:
            raise ValidationError({'message': 'You cannot update other users!'})
        if serializer.instance.status != 'PENDING':
            raise ValidationError({'message': 'Cannot update non-pending requests'})
        serializer.save()


class FriendListView(ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def list(self, request, *args, **kwargs):
        friend_requests = FriendRequest.objects.filter(Q(status='ACCEPTED') & (Q(from_user=self.request.user) | Q(to_user=self.request.user)))
        from_user_list = friend_requests.values_list('from_user', flat=True)
        to_user_list = friend_requests.values_list('to_user', flat=True)
        
        from_user_list = friend_requests.values_list('from_user', flat=True)
        to_user_list = friend_requests.values_list('to_user', flat=True)
    
        # Remove self.user.id from both lists
        self_user_id = self.request.user.id
        from_user_list = [user_id for user_id in from_user_list if user_id != self_user_id]
        to_user_list = [user_id for user_id in to_user_list if user_id != self_user_id]

        from_users = get_user_model().objects.filter(id__in=from_user_list).values('id', 'username', 'email')
        to_users = get_user_model().objects.filter(id__in=to_user_list).values('id', 'username', 'email')

        merged_users = list(from_users) + list(to_users)

        merged_users = [user for user in merged_users if user]
        return Response({"friends": merged_users})


class PendingFriendRequestListView(ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def list(self, request, *args, **kwargs):
        user_id = self.request.user.id
        
        # Fetch pending friend requests where the user is either the sender or the receiver
        friend_requests = FriendRequest.objects.filter(status='PENDING').filter(
            Q(from_user_id=user_id) | Q(to_user_id=user_id)
        )
        
        # Construct the response data
        pending_requests_recieved = []
        pending_requests_sent = []
        for friend_request in friend_requests:
            if friend_request.from_user_id == user_id:
                pending_request_data = {
                    'id': friend_request.id,
                    'user': {
                        'id': friend_request.to_user.id,
                        'username': friend_request.to_user.username,
                        'email': friend_request.to_user.email
                    }
                }
                pending_requests_sent.append(pending_request_data)
            elif friend_request.to_user_id == user_id:
                pending_request_data = {
                    'id': friend_request.id,
                    'user': {
                        'id': friend_request.from_user.id,
                        'username': friend_request.from_user.username,
                        'email': friend_request.from_user.email
                    }
                }
                pending_requests_recieved.append(pending_request_data)

        return Response({"pending-sent": pending_requests_sent, "pending-received": pending_requests_recieved})

