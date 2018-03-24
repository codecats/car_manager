from django.forms import forms, ModelForm, IntegerField

from manager.controller import CarController
from manager.models import Car, Battery


class CarChangeForm(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class CarAddForm(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

    batteries_count = IntegerField(initial=5, required=True)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.save()
        n = self.cleaned_data.get('batteries_count', 0)
        oddnumbers = CarController.generate_odd_numbers(n)
        for i in range(self.cleaned_data.get('batteries_count', 0)):
            Battery(car=instance, number=i + 1, ID=oddnumbers[i]).save()
        return instance


class BatteryForm(ModelForm):
    class Meta:
        model = Battery
        fields = '__all__'

    def clean(self):
        car = self.cleaned_data.get('car', None)
        if car is not None:
            id_ = self.cleaned_data.get('ID', None)
            number = self.cleaned_data.get('number', None)
            for key, val in {'ID': id_, 'number': number}.items():
                query = car.batteries.filter(**{key: val})
                if self.instance is not None:
                    query = query.exclude(pk=self.instance.pk)
                if query.exists():
                    raise forms.ValidationError("{} must be unique".format(key))
        return self.cleaned_data
