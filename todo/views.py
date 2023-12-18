from .serializers import ToDoSerializer
from .models import ToDo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .permissions import IsOwnerOrReadOnly


# Create your views here.


class ToDoList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    serializer_class = ToDoSerializer
    def get(self, request):
        snippets = ToDo.objects.filter(owner=request.user)
        serializer = self.serializer_class(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        snippet = request.data
        serializer = self.serializer_class(data=snippet)
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    serializer_class = ToDoSerializer

    @staticmethod
    def get_object(pk):
        try:
            return ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = self.serializer_class(todo, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status.HTTP_204_NO_CONTENT)

