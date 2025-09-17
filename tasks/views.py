from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from .models import Task
from .serializers import RegisterSerializer, TaskSerializer

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(owner=user) | Q(assignee=user)).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.owner != request.user:
            raise PermissionDenied(detail="Only the task owner can edit the task.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.owner != request.user:
            raise PermissionDenied(detail="Only the task owner can partially update the task.")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.owner != request.user:
            raise PermissionDenied(detail="Only the task owner can delete the task.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        if task.owner != request.user:
            raise PermissionDenied(detail="Only the owner can assign this task.")

        assignee_id = request.data.get('assignee_id')
        if not assignee_id:
            return Response({'detail': 'assignee_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            assignee = User.objects.get(pk=assignee_id)
        except User.DoesNotExist:
            return Response({'detail': 'Assignee not found.'}, status=status.HTTP_404_NOT_FOUND)

        task.assignee = assignee
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        task = self.get_object()
        if task.assignee != request.user:
            raise PermissionDenied(detail="Only the assignee can update the status.")

        new_status = request.data.get('status')
        if new_status not in dict(Task.STATUS_CHOICES).keys():
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = new_status
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
