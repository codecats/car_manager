from django.core.validators import MinValueValidator
from django.db.models import Model, CharField, AutoField, PositiveIntegerField, BooleanField, ForeignKey, \
    CASCADE

from manager.validators import validate_odd


class PrimaryKeyModel(Model):
    class Meta(object):
        abstract = True

    primary_id = AutoField(primary_key=True)


class Car(PrimaryKeyModel):
    ID = CharField(unique=True, max_length=255, db_index=True)
    name = CharField(max_length=50, db_index=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.ID)


class Battery(PrimaryKeyModel):
    MIN_ID = 5
    car = ForeignKey(Car, related_name='batteries', on_delete=CASCADE)
    number = PositiveIntegerField(default=1, db_index=True, validators=[MinValueValidator(1)])
    ID = PositiveIntegerField(default=MIN_ID, db_index=True, validators=[MinValueValidator(MIN_ID), validate_odd])
    is_on = BooleanField(default=True)

    def __str__(self):
        return 'ID: {} / Number {}'.format(self.ID, self.number)
