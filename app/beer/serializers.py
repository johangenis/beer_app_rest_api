from rest_framework import serializers

from core.models import Tag, Beer, Review


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_Fields = ("id",)


class BeerSerializer(serializers.ModelSerializer):
    """Serializer for a beer object"""

    class Meta:
        model = Beer
        fields = (
            "id",
            "name",
            "ibu",
            "calories",
            "abv",
            "style",
            "brewery_location",
        )
        read_only_fields = ("id",)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for a review object"""

    class Meta:
        model = Review
        fields = ("id", "name", "aroma", "appearance", "taste", "overall")
        read_only_fields = ("id",)
