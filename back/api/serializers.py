from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.gis.geos import Polygon
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .models import (
    Copyright, Document, Format, Identity,
    Metadata, MetadataContact, Order, OrderItem, OrderType,
    Pricing, Product, ProductFormat)

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from allauth.account.adapter import get_adapter


# Get the UserModel
UserModel = get_user_model()


class CopyrightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Copyright
        fields = '__all__'


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class FormatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'


class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = '__all__'


class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        exclude = ['password']


class MetadataIdentitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Identity
        fields = [
            'url',
            'first_name', 'last_name', 'email',
            'phone', 'street', 'street2',
            'company_name',
            'postcode', 'city', 'country']


class MetadataContactSerializer(serializers.HyperlinkedModelSerializer):
    contact_person = MetadataIdentitySerializer(read_only=True)
    class Meta:
        model = MetadataContact
        fields = [
            'contact_person',
            'metadata_role']

# TODO: Test this, check for passing contexts ! Check public identities
class MetadataSerializer(serializers.HyperlinkedModelSerializer):
    contact_persons = serializers.SerializerMethodField()
    modified_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Metadata
        fields = '__all__'

    def get_contact_persons(self, obj):
        """obj is a Metadata instance. Returns list of dicts"""
        qset = MetadataContact.objects.filter(metadata=obj)
        return [
            MetadataContactSerializer(m, context={
                'request': self.context['request']
                }).data for m in qset]


class OrderDigestSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer showing a summary of an Order.
    Always exclude geom here as it is used in lists of
    orders and performance can be impacted.
    """
    order_type = serializers.StringRelatedField()
    class Meta:
        model = Order
        exclude = [
            'geom', 'date_downloaded', 'client',
            'processing_fee_currency', 'processing_fee',
            'part_vat_currency', 'part_vat',
            'order_contact', 'invoice_contact']


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    A Basic serializer for order items
    """
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemTextualSerializer(serializers.ModelSerializer):
    """
    A more human-readable serializer replacing ids by labels.
    """
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='label')
    format = serializers.SlugRelatedField(
        queryset=Format.objects.all(),
        slug_field='name')

    class Meta:
        model = OrderItem
        exclude = ['order']


class OrderSerializer(serializers.ModelSerializer):
    """
    A complete Order serializer.
    """
    order_type = serializers.SlugRelatedField(
        queryset=OrderType.objects.all(),
        slug_field='name',
        help_text='Input the translated string value, for example "Privé"')
    items = OrderItemTextualSerializer(many=True)
    client = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Order
        exclude = ['date_downloaded']
        read_only_fields = [
            'date_ordered', 'date_processed',
            'processing_fee_currency', 'processing_fee',
            'total_cost_currency', 'total_cost',
            'part_vat_currency', 'part_vat',
            'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        geom = validated_data.pop('geom')
        order = Order(**validated_data)
        order.geom = Polygon(geom.coords[0], srid=2056)
        order.save()
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        geom = validated_data.pop('geom', None)

        if geom:
            instance.geom = Polygon(geom.coords[0], srid=2056)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)
        return instance


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'domain_override': getattr(settings, 'FRONT_URL'),
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for setting a new user password.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(urlsafe_base64_decode(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()


class PricingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        exclude = ['ts']


class ProductFormatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductFormat
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        identity = Identity(**validated_data)
        identity.set_password(password)
        identity.save()
        return identity

    class Meta:
        model = Identity
        exclude = [
            'password', 'last_login', 'date_joined',
            'groups', 'user_permissions', 'is_staff',
            'is_active', 'is_superuser', 'sap_id',
            'contract_accepted']


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()
