from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from manager.controller import CarController
from manager.models import Car, Battery


class AssemblyTestCase(TestCase):
    def setUp(self):
        pass

    def test_car_creation_unique_id(self):
        Car(name='William', ID='zv-123').save()
        with self.assertRaises(IntegrityError):
            Car(name='Dolores', ID='zv-123').save()

    def test_unique_batteries_per_car(self):
        c1 = Car(name='William', ID='zv-123')
        c2 = Car(name='Dolores', ID='zv-3w1')
        c1.save()
        c2.save()
        b1c1 = Battery(car=c1, ID=342)
        b1c2 = Battery(car=c1, ID=342)
        b1c1.save()
        b1c2.save()


    def test_odd_number_generator(self):
        odds = CarController.generate_odd_numbers(1000)
        for odd in odds:
            self.assertEqual(odd % 2, 1)