from django.db import models

from articles.models import Tag
from stats_api.models import Player, Team


class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    former_club = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='out_transfers')
    destination_club = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='in_transfers')
    date = models.DateField()
    cost = models.DecimalField(max_digits=11, decimal_places=2)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return '{0} from {1} to {2}'.format(self.player.name, self.former_club.name, self.destination_club.name)

