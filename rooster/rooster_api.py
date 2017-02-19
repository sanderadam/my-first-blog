from rest_framework import serializers
from .models import Dienst, Chauffeur

'''
class DienstSerializer(serializers.Serializer):
    beschrijving = serializers.CharField(max_length=200)
    comments = serializers.CharField(max_length=1000)
    date = serializers.DateField()
    begintijd = serializers.TimeField()
    eindtijd = serializers.TimeField()
    feestdagen = serializers.FloatField(default = 1)


    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.beschrijving = validated_data.get('beschrijving', instance.beschrijving)

'''
class DienstSerializer(serializers.ModelSerializer):
    #tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Dienst
        fields = '__all__'
        #fields = ('beschrijving', 'comments', 'date', 'begintijd','eindtijd','chauffeur')
        depth = 1
