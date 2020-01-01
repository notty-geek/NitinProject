from django.shortcuts import render
from blogging.models import Blog
from django.http import Http404
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from blogging.models import Blog
from blogging.serializers import BlogSerializer
from rest_framework import permissions
from blogging.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import User
from rest_framework import authentication
from copy import deepcopy
from datetime import timezone
import time
import datetime


class BlogView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get(self,request):
        limit = request.query_params.get('limit', None)
        if limit:
            snippets = Blog.objects.all().only("id", "createdAt","name")[:int(limit)]
        else:
            snippets = Blog.objects.all().only("id", "createdAt","name")
        serializer = BlogSerializer(snippets, many=True)
        data = deepcopy(serializer.data)
        for i in data:
            dt = i.get('createdAt',None)
            new_dt = dt[:19]
            dt = datetime.datetime.strptime(new_dt, '%Y-%m-%d %H:%M:%S')
            i['createdAt'] = dt.timestamp()
            i.pop('id')

        return JsonResponse(data, safe=False)

    def post(self,request):
        data = JSONParser().parse(request)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({"id": serializer.data.get("id")}, status=201)
        return JsonResponse(serializer.errors, status=400)

class BlogViewById(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get(self,request, id):
        """
        Retrieve, update or delete a code snippet.
        """
        try:
            snippet = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return JsonResponse({"Error":"No Blog Found"}, status=400)

        serializer = BlogSerializer(snippet)
        data = deepcopy(serializer.data)
        dt = data.get('createdAt', None)
        new_dt = dt[:19]
        dt = datetime.datetime.strptime(new_dt, '%Y-%m-%d %H:%M:%S')
        data['createdAt'] = dt.timestamp()
        data['content'] = snippet.content
        data.pop("id")
        return JsonResponse(data)

    def put(self,request,id):
        try:
            snippet = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return JsonResponse({"Error": "No Blog Found"}, status=400)

        data = JSONParser().parse(request)
        print(data)
        serializer = BlogSerializer(snippet, data=data)
        if serializer.is_valid():
            print ("Valid")
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors, status=400)

    def delete(self,request,id):
        try:
            snippet = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return JsonResponse({"Success": "Blog Already Deleted"}, status=200)

        snippet.delete()
        return JsonResponse({"Success": "{id} Blog Deleted".format(id=id)}, status=200)