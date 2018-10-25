from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, FileField


class BulkUploadCsvSerializer(Serializer):
    file = FileField(required=True)

    def validate(self, attrs):
        if 'file' in attrs:
            if attrs['file'].name.endswith('.csv'):
                # valid
                return attrs

            # the file should be csv
            raise ValidationError({'file': 'file extension should be .csv'})

        # the file is missing
        raise ValidationError({'file': 'file is required'})
