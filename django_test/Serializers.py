from rest_framework import serializers
from django_test.models import Molong, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User
# LANGUAGE_CHOICES, STYLE_CHOICES => code highlighting options

class MolongSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    owner = serializers.ReadOnlyField(source='owner.username')  # owner 필드의 값에서 참조하고 있는 model 내부의 특정 필드로 지정해줄 수 있음
    class Meta:
        model = Molong
        fields = ['id',
                  'title',
                  'code',
                  'linenos',
                  'language',
                  'style',
                  'owner', # 추가해주어야 함
                  'highlighted']
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Molong.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

class BurgerSerializers(serializers.Serializer):
    name = serializers.CharField(required=True)
    price = serializers.IntegerField(default=0)
    calories = serializers.IntegerField(default=0)

class UserSerializer(serializers.ModelSerializer):
    molong = serializers.PrimaryKeyRelatedField(many=True, queryset=Molong.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'molong']