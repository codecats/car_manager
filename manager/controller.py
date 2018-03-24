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
    def battery(self):
        '''
        always return battery with greatest number
        :return:
        '''
        return self.car.batteries.all().order_by('-number').first()

    def setup_unique_battery(self, instance):
        # get initial number and id based on already existing batteries
        if self.id is None:
            # we are sure that number is unique because of ordering in battery property
            if self.battery is not None:
                self.number, self.id = self.battery.number + 1, self.battery.ID + 2
            else:
                self.number, self.id = 1, Battery.MIN_ID
        # this battery don't have ID, saved instances is set up
        if instance.pk is None:
            # probably ID is unique but we have to check for the reason if somebody changed it manually
            while self.car.batteries.filter(ID=self.id).exists():
                self.id += 2
            instance.number, instance.ID = self.number, self.id
            self.number += 1
            self.id += 2
        return instance
