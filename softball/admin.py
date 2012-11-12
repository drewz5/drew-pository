from django.contrib import admin

from models import Team, Player, Game, Roster, Statistic

class GameAdmin(admin.ModelAdmin):
     fields = ('played_on', 'location', 'home_roster', 'away_roster')
     max_num = 12
     extra = 12

class PlayerAdmin(admin.ModelAdmin):
    fields = ('name', 'number', 'team',)
    max_num = 12
    extra = 12

class TeamAdmin(admin.ModelAdmin):
     fields = ('name',)
     max_num = 12
     extra = 12

class RosterAdmin(admin.ModelAdmin):
     fields = ('team',)
     max_num = 12
     extra = 12

admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Roster, RosterAdmin)
