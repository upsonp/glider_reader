from django.db import models


class Mission(models.Model):

    mission_number = models.IntegerField(verbose_name="Mission #")


class Glider(models.Model):

    mission = models.ForeignKey(Mission, verbose_name="Mission #", related_name="gliders", on_delete=models.CASCADE,
                                default=1)
    label = models.CharField(max_length=12, verbose_name="Glider Label")

    def __str__(self):
        return self.label