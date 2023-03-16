from django.contrib import admin

# Register your models here.
from stats_api.models import *


admin.site.register(Tournament)
admin.site.register(TournamentSeason)
admin.site.register(Manager)
admin.site.register(Stadium)
admin.site.register(Team)
admin.site.register(Referee)
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(Goal)
admin.site.register(Booking)
admin.site.register(Substitution)
admin.site.register(TeamMatchStats)
admin.site.register(PlayerMatchStats)
admin.site.register(GoalType)
admin.site.register(TeamTournamentStats)
