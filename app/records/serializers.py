from rest_framework import serializers
from records.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'date', 'time_spent', 'student_id', 'subject_id')