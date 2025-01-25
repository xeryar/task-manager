from rest_framework import serializers


def get_base_model_fields() -> list[str]:
    return [
        "description",
        "created_at",
        "updated_at",
    ]


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = get_base_model_fields()
        read_only_fields = (
            "created_at",
            "updated_at",
        )
