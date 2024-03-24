from .models import Movie
from ninja import ModelSchema, Schema


class MovieIn(ModelSchema):
    class Meta:
        model = Movie
        exclude = ["id", "created_at", "modified_at"]
        fields_optional = "__all__"


class MovieOut(ModelSchema):
    class Meta:
        model = Movie
        fields = "__all__"
        fields_optional = "__all__"


class ExtraMessage(Schema):
    message: str
