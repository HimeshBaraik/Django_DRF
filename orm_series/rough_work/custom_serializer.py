from rest_framework import serializers
from .models import YourModel

class CustomSerializer(serializers.ModelSerializer):
    """
    A custom serializer template for your model.
    
    This template includes:
    - Field validation
    - Object-level validation
    - Custom field transformations (e.g., `to_internal_value`)
    - Custom representation (e.g., `to_representation`)
    """

    # You can add custom fields if needed
    custom_field = serializers.CharField(write_only=True)  # Example of a custom field

    class Meta:
        model = YourModel  # Specify the model you are serializing
        fields = '__all__'  # Or specify the fields you want to serialize explicitly

    # ========= Field-Level Validation (Custom Validation on Individual Fields) =========

    def validate_custom_field(self, value):
        """
        Custom validation for a specific field (e.g., `custom_field`).
        """
        if not value.isupper():
            raise serializers.ValidationError("This field must be in uppercase.")
        return value

    # ========= Object-Level Validation (Validating Multiple Fields Together) =========

    def validate(self, attrs):
        """
        Custom object-level validation for multiple fields.
        This is useful when validation depends on more than one field.
        """
        # Example: Ensure `start_date` is earlier than `end_date`
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("Start date must be before end date.")
        
        # Add any other validation logic here

        return attrs

    # ========= Custom Conversion of Input Data (to_internal_value) =========

    def to_internal_value(self, data):
        """
        Customize how incoming data is transformed into Python types.
        This is useful for preprocessing before validation.
        """
        # Example: Convert incoming date string to a Python `datetime.date` object
        if 'date_field' in data:
            data['date_field'] = self.convert_string_to_date(data['date_field'])

        # Example: Manipulate incoming field data before validation
        if 'some_field' in data:
            data['some_field'] = data['some_field'].lower()  # Normalize the value to lowercase

        return super().to_internal_value(data)

    def convert_string_to_date(self, date_string):
        """
        Convert a string in 'YYYY-MM-DD' format to a Python `datetime.date` object.
        """
        from datetime import datetime
        return datetime.strptime(date_string, '%Y-%m-%d').date()

    # ========= Custom Representation of Output Data (to_representation) =========

    def to_representation(self, instance):
        """
        Customize how the model instance is represented when sending data back to the client.
        """
        representation = super().to_representation(instance)

        # Example: Add a custom field to the serialized output
        representation['formatted_date'] = instance.date_field.strftime('%B %d, %Y')  # Custom formatted date

        # Example: Add computed field (e.g., calculate a derived value)
        representation['full_name'] = f"{instance.first_name} {instance.last_name}"

        # Example: Remove or hide certain fields dynamically
        if instance.some_field == 'some_condition':
            representation.pop('unwanted_field', None)

        return representation

