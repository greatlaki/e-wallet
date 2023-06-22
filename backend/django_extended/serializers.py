from rest_framework import serializers


class ReadableHiddenField(serializers.HiddenField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write_only = False

    def to_representation(self, value):
        if hasattr(value, "id"):
            return value.id
        return value
