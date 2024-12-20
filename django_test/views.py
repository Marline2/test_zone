from django.shortcuts import render

def main(request):
    return render(request, 'main.html')

def burger_list(request):
    return render(request, 'burger_list.html')
# Create your views here.
from rest_framework.response import Response
from rest_framework import status, generics
from django_test.models import (Molong)
from django_test.Serializers import MolongSerializer, UserSerializer
from rest_framework.views import APIView
from django.http import Http404
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth.models import User
from rest_framework import permissions
class MolongList(APIView):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get(self, request, format=None):
        molong = Molong.objects.all()
        serializer = MolongSerializer(molong, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MolongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, staus=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Molong, self).save(*args, **kwargs)

class MolongDetail(APIView):
    def get_object(self, pk):
        try:
            return Molong.objects.get(pk=pk)
        except Molong.DoseNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        molong = self.get_object(pk)
        serializer = MolongSerializer(molong)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        molong = self.get_object(pk)
        serializer = MolongSerializer(molong, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        molong = self.get_object(pk)
        molong.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer