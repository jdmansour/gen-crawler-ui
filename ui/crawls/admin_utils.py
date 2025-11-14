

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import (RelatedFieldWidgetWrapper)
from django.db.models.base import Model
from django.db.models.fields.related import ManyToOneRel
from django.forms import ModelChoiceField
from .models import Crawler, FilterSet


class ReverseModelChoiceField(ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widget = RelatedFieldWidgetWrapper(
            self.widget,
            FieldWrapper(Crawler._meta.get_field('filter_set').remote_field),
            admin.site,
            can_add_related=True, can_change_related=True, can_view_related=True)

    def validate(self, value: FilterSet | None) -> None:
        """ Ensure that the selected FilterSet is not already used by another Crawler. """
        
        if value and value.crawler is not None:
            raise forms.ValidationError(
                f"FilterSet '{value}' is already used by crawler '{value.crawler}'. "
                "Each FilterSet can only be associated with one crawler."
            )

        return super().validate(value)

    def save_related(self, instance: Crawler, filter_set: FilterSet) -> None:
        """ Save the related FilterSet to point to the given Crawler instance.
            Call this after saving the main instance in the form. """
        if instance.pk:
            if old_filter_set := getattr(instance, "filter_set", None):
                old_filter_set.crawler = None
                old_filter_set.save()

        if filter_set is not None:
            filter_set.crawler = instance
            filter_set.save()

    def label_from_instance(self, obj: Model) -> str:
        label = super().label_from_instance(obj)
        if obj.crawler is not None:
            return f"{label} (used by crawler '{obj.crawler}')"
        return label


class FieldWrapper:
    """ Hack: Wraps a OneToOneField and adds get_related_field().
        It would proably be better to make a custom ForeignObjectRel subclass. """
    
    def __init__(self, field: ManyToOneRel):
        self.field = field

    def get_related_field(self):
        return self.field.model._meta.get_field('id')
    
    @property
    def limit_choices_to(self):
        return None

    # pass through other attributes
    def __getattr__(self, name):
        return getattr(self.field, name)
