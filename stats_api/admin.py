from django.contrib import admin

# Register your models here.
from stats_api.models import Player, Team, Transfer, Popularities

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Transfer)
admin.site.register(Popularities)
