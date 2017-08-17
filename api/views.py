from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import UploadSerializer
from api.models import FilesModel


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'files': reverse('files-list', request=request, format=format),
    })


class FileListView(generics.ListCreateAPIView):
    """The view set for file creation and upload"""
    queryset = FilesModel.objects.all()
    serializer_class = UploadSerializer


class FileSearchView(APIView):
    """The view set for file searching"""
    def get_objects(self, name):
        try:
            if name: return FilesModel.objects.filter(name__icontains=name)
            return FilesModel.objects.all()
        except FilesModel.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        files = self.get_objects(request.GET.get('q', ''))
        serializer = UploadSerializer(files, many=True)
        return Response(serializer.data)


class FileDetailView(APIView):
    """ Retrieve and delete a file """
    def get_object(self, pk):
        try:
            return FilesModel.objects.get(pk=pk)
        except FilesModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = UploadSerializer(file)
        return Response(serializer.data)


    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
