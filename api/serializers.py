from rest_framework import serializers
from .models import User  # o tu modelo personalizado
import re


ALLOWED_DOMAINS = ['gmail.com', 'duoc.cl', 'yahoo.com']

class RegisterSerializer(serializers.ModelSerializer):
    conf_pass = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
             "first_name", "last_name", "second_last_name",
            "rut", "email", "phone", "address", "password","conf_pass"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["conf_pass"]:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

    def validate_email(self, value):
            domain = value.split('@')[-1]
            if domain not in ALLOWED_DOMAINS:
                raise serializers.ValidationError("Solo se permiten correos de Gmail, Duoc o Yahoo.")
            return value
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Debe incluir al menos una letra mayúscula.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Debe incluir al menos un número.")
        if not re.search(r'[\W_]', value):
            raise serializers.ValidationError("Debe incluir al menos un símbolo (como @, #, !).")
        return value

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']  # Usa email como username
        validated_data.pop('conf_pass')  # Elimina el campo no necesario para crear el usuario
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

