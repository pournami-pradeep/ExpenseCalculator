from rest_framework import serializers

from monthlyexpenses.models import Source


class SourceSerializer(serializers.ModelSerializer):
    label = serializers.CharField(max_length=30, required=True)

    def validate_label(self, label):
        if Source.objects.filter(label=label).exists():
            raise serializers.ValidationError("Source with this label already exist.")
        return label

    class Meta:
        model = Source
        fields = ("id","label",)
