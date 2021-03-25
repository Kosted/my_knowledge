from django.db.models import F
from rest_framework import serializers

from knowledge.models import Memory, Tag, RegularUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        # fields = "__all__"

    def create(self, validated_data):
        return RegularUser.objects.create_user(**validated_data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['tag_text', 'count']
        read_only_fields = ['count']


class TagList(serializers.Serializer):
    def update(self, instance, validated_data):
        # super().update()
        pass

    def create(self, validated_data):
        pass

    tags = serializers.ListSerializer(child=serializers.CharField(max_length=50))

    def validate(self, attrs):
        request_tags = set(attrs['tags'])
        db_tags = Tag.objects.filter(user=self.initial_data['user'], tag_text__in=attrs['tags'])
        exists_tags = set([tag.tag_text for tag in db_tags])
        for tag in request_tags:
            if tag not in exists_tags:
                raise serializers.ValidationError(detail=f'{tag} doesnt exists')
        attrs['tags'] = db_tags
        return attrs


class MemorySerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=TagSerializer(), required=False)

    class Meta:
        model = Memory
        fields = ['id', 'user', 'memory_text', 'tags', 'priority', ]
        read_only_fields = ['id', ]
        extra_kwargs = {'user': {'write_only': True}}

    def validate_memory_text(self, value):
        if Memory.objects.filter(memory_text=value, user=self.initial_data['user']).exists():
            raise serializers.ValidationError(detail='Memory already exists')
        return value

    def create(self, validated_data):
        memory = Memory.objects.create(user=validated_data['user'],
                                       memory_text=validated_data['memory_text'],
                                       priority=validated_data['priority'])

        tags_texts = set(tag['tag_text'] for tag in validated_data['tags'])

        exists_tags = Tag.objects.filter(user=validated_data['user'], tag_text__in=tags_texts)

        new_tags_texts = set(tags_texts).difference((tag.tag_text for tag in exists_tags))
        exists_tags.update(count=F('count') + 1)

        new_tags = Tag.objects.bulk_create(
            [Tag(tag_text=tag_text, user=validated_data['user']) for tag_text in new_tags_texts]
        )

        for tag in new_tags:
            memory.tags.add(tag)
        for tag in exists_tags:
            memory.tags.add(tag)

        return memory

    def update(self, instance, validated_data):

        instance.memory_text = validated_data['memory_text']

        instance.priority = validated_data['priority']

        tags_texts = set(tag['tag_text'] for tag in validated_data['tags'])

        memory_exists_tags = instance.tags.all()
        memory_exists_tags_texts = set(tag.tag_text for tag in memory_exists_tags)
        tags_texts_for_delete = memory_exists_tags_texts.difference(tags_texts)

        exists_user_tags = Tag.objects.filter(user=validated_data['user'], tag_text__in=tags_texts)

        exists_user_tags_texts_to_add = tags_texts.intersection(
            set(tag.tag_text for tag in exists_user_tags)).difference(memory_exists_tags_texts)

        new_tags_texts = tags_texts.difference((tag.tag_text for tag in exists_user_tags))

        new_tags = Tag.objects.bulk_create(
            [Tag(tag_text=tag_text, user=validated_data['user']) for tag_text in new_tags_texts]
        )

        tags_to_delete = []

        for tag_text in tags_texts_for_delete:
            for tag in memory_exists_tags:
                if tag_text == tag.tag_text:
                    tags_to_delete.append(tag)
                    break

        for tag in new_tags:
            instance.tags.add(tag)

        for tag in tags_to_delete:
            instance.tags.remove(tag)

        Tag.objects.filter(id__in=[tag.id for tag in tags_to_delete]).update(count=F('count') - 1)

        instance.save()

        return instance
