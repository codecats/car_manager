from django.contrib import admin

from manager.controller import CarController
from manager.forms import CarChangeForm, CarAddForm, BatteryForm
from manager.models import Car, Battery


@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    form = BatteryForm


class BatteryInline(admin.TabularInline):
    model = Battery
    fields = ['is_on']
    extra = 0


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('ID', 'name', 'get_battery_on_count', 'get_battery_all_count')
    form = CarChangeForm
    add_form = CarAddForm

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            self.inlines = [BatteryInline]
            return self.form
        return self.add_form

    def get_battery_on_count(self, instance):
        return instance.batteries.filter(is_on=True).count()

    get_battery_on_count.short_description = 'Batteries ON'

    def get_battery_all_count(self, instance):
        return instance.batteries.all().count()

    get_battery_all_count.short_description = 'All Batteries'

    def save_formset(self, request, form, formset, change):
        ctl = None
        for form in formset:
            instance = form.save(commit=False)
            if ctl is None:
                ctl = CarController(instance.car)
            instance = ctl.setup_unique_battery(instance)
            instance.save()

        return super().save_formset(request, form, formset, change)