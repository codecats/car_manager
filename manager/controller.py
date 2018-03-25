from random import sample

from django.utils.functional import cached_property

from manager.models import Battery


class CarController(object):
    id = None
    number = None
    car = None

    def __init__(self, car):
        self.car = car

    @classmethod
    def generate_odd_numbers(cls, n=5):
        '''
        generate n-odd numbers
        :param n: int
        :return: list
        '''
        return sorted(sample(range(Battery.MIN_ID, Battery.MIN_ID + (n * 2), 2), n))

    @cached_property
    def battery_number(self):
        '''
        always return battery with greatest number
        :return:
        '''
        return getattr(self.car.batteries.all().order_by('-number').first(), 'number', 0)

    @cached_property
    def battery_id(self):
        '''
        always return battery with greatest number
        :return:
        '''
        return getattr(self.car.batteries.all().order_by('-ID').first(), 'ID', Battery.MIN_ID - 2)

    def setup_unique_battery(self, instance):
        # get initial number and id based on already existing batteries
        if self.id is None:
            # we are sure that number is unique because of ordering in battery property
            self.number, self.id = self.battery_number + 1, self.battery_id + 2
        # this battery don't have ID, saved instances is set up
        if instance.pk is None:
            instance.number, instance.ID = self.number, self.id
            self.number += 1
            self.id += 2
        return instance
