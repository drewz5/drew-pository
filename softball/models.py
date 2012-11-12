from django.db import models

from django.db.models import Sum

from decimal import Decimal 
"""classes are generally initCap"""
import calc


class Team(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, db_index=True)


    def __unicode__(self):
        return self.name


    def player_count(self):
        pass


class Player(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, unique=True)
    number = models.PositiveIntegerField()
    team = models.ForeignKey('Team', related_name='players')

    class Meta:
        ordering = ["name", ]

    def __unicode__(self):
        return u'{0} #{1} - {2}'.format(self.name,
                                        self.number or 'N/A',
                                        self.team.name)

    @property
    def hits(self):
        return sum(filter(None,
            self.statistics.aggregate(django.db.models.Sum('singles'),
                                      django.db.models.Sum('doubles'),
                                      django.db.models.Sum('triples'),
                                      django.db.models.Sum('home_runs'),)))
#filter:pass in a method (i.e. None; x > 5; etc) and it will pass the values in to the method
#to determine whether you want to keep particular value
#will explicitly remove all "None's" from the list, in this case

        """
Returns the total hits, doubles, triples, and home_runs
"""
        pass


    @property
    def walks(self):
        """
Returns the total number of walks for this player
"""
        pass


    @property
    def runs(self):
       # return self.statistics.values_list('runs', 'hits') #flat=True x tupples
        #return sum(self.statistics.values_list('runs'))
        # return self.statistics.aggregate(Sum('runs')) (gives a dictionary)
        #return self.statistics.aggregate(s=Sum('runs'))
        #will return dictionary as {'s':123}
        return self.statistics.aggregate(s=Sum('runs'))['s'] or 0 #gives an integer

        """
Returns the total number of walks for this player
***RELATED_NAME provides reverse relationship on a table
***so for player, we can look at the Statistic table, where 
   the related_name is 'statistics'
"""
        pass


    def singles(self):
        return self.statistics.aggregate(s=Sum('singles'))['s'] or 0      
        """
Returns the total number of walks for this player
"""
        pass


    @property
    def at_bats(self):
        """
Returns the total number of walks for this player
"""
        pass


    @property
    def doubles(self):
        """
Returns the total number of walks for this player
"""
        pass


    @property
    def triples(self):
        """
Returns the total number of walks for this player
"""
        pass


    @property
    def home_runs(self):
        """
Returns the total number of home runs for this player
"""
        pass


    @property
    def rbis(self):
        """
Returns the total number of rbis for this player
"""
        pass


    @property
    def batting_average(self):
        pass


    @property
    def on_base_percentage(self):
        pass

    @property
    def slugging_percentage(self):
        pass


class Game(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    played_on = models.DateTimeField()
    location = models.CharField(max_length=150)
    home_roster = models.OneToOneField('Roster', related_name='home_game')
    away_roster = models.OneToOneField('Roster', related_name='away_game')


    def __unicode__(self):
        return u'{0} - {1}'.format(self.location, self.played_on)


    @property
    def winner(self):
        pass


    @property
    def final_score(self):
        """
Returns the final score of the game, as recorded in the rosters, as a
tuple (away_score, home_score)
"""
        pass


    @property
    def home_score(self):
        """
Returns the score of the home team, as recorded in the home roster
"""
        pass


    @property
    def away_score(self):
        """
Returns the score of the home team, as recorded in the home roster
"""
        pass


class Roster(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    team = models.ForeignKey('Team', related_name='rosters')


    def __unicode__(self):
        return '{0} - {1}'.format(self.team.name, self.id)


class Statistic(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    player = models.OneToOneField('Player', related_name='statistics')
    at_bats = models.PositiveIntegerField(default=0)
    runs = models.PositiveIntegerField(default=0)
    singles = models.PositiveIntegerField(default=0)
    doubles = models.PositiveIntegerField(default=0)
    triples = models.PositiveIntegerField(default=0)
    home_runs = models.PositiveIntegerField(default=0)
    rbis = models.PositiveIntegerField(default=0)
    walks = models.PositiveIntegerField(default=0)
    roster = models.ForeignKey('Roster', related_name='player_statistics')


    def __unicode__(self):
        return u'{0} - {1}'.format(self.player.name, self.roster)


    @property
    def hits(self):
        return self.singles + self.doubles + self.triples + self.home_runs


    @property
    def batting_average(self):
        if self.at_bats == 0:
            return Decimal("0")
        return Decimal(self.hits()) / Decimal(self.at_bats)
        """return self.hits() / float(self.at_bats)
       Must add "float" or "Decimal" before so the value doesn't get rounded
        """
        """
        if self.at_bats > 0:
           return Decimal(self.hits()) / Decimal(self.at_bats)
            else:
                -or raise Exception("No division by zero!")
                return Decimal("0")
                - implicit return none for any method
            """
       
