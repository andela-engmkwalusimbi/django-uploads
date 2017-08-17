from rest_framework import serializers
from api.models import FilesModel

class UploadSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class that defines meta data info about the serializer class"""
        model = FilesModel
        fields = ( 'id', 'image', 'name', 'size', 'date_modified', )
        read_only_fields = ('name', 'size', 'date_modified',)
