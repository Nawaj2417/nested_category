from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    children_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name','parent','children', 'children_data']
        extra_kwargs = {
            'children': {'write_only': True},
            'children_data': {'read_only': True},
        }

    def create(self, validated_data):
        # Extract children data
        children_data = validated_data.pop('children', [])
        # Create the parent category
        category = Category.objects.create(**validated_data)

        # Recursively create child categories
        for child_data in children_data:
            child_data['parent'] = category
            self.create(child_data)

        return category

    def update(self, instance, validated_data):
        # Update the parent category fields
        instance.name = validated_data.get('name', instance.name)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()

        # Handle children data
        children_data = validated_data.pop('children', [])
        existing_children = {child.id: child for child in instance.children.all()}

        for child_data in children_data:
            child_id = child_data.get('id')
            if child_id and child_id in existing_children:
                # Update existing child
                self.update(existing_children[child_id], child_data)
            else:
                # Create new child
                child_data['parent'] = instance
                self.create(child_data)

        return instance

    def get_children_data(self, obj):
        children = obj.children.filter(is_deleted=False)
        return CategorySerializer(children, many=True).data
