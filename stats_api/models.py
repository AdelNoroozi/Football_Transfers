from datetime import datetime, date

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from utils.models import Country, City


class Tournament(models.Model):
    TOURNAMENT_TYPES = (('L', 'league'),
                        ('KO', 'knockout'),
                        ('C', 'combination'))
    host = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='tournaments')
    type = models.CharField(max_length=10, choices=TOURNAMENT_TYPES)


class TournamentSeason(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.RESTRICT, related_name='seasons')
    season = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_teams = models.IntegerField()


class Manager(models.Model):
    name = models.CharField(max_length=50)
    nationality = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='managers')
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)


class Stadium(models.Model):
    name = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, related_name='stadiums')
    capacity = models.IntegerField()


class Team(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField(max_length=500)
    president = models.CharField(max_length=50)
    open_transfer_window = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='teams')
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='teams')
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name='teams')
    tournaments = models.ManyToManyField(Tournament)

    def __str__(self):
        return self.name

    def no_of_scores(self):
        scores = Popularities.objects.filter(team=self)
        return len(scores)

    def avg_score(self):
        sum = 0
        scores = Popularities.objects.filter(team=self)
        for score in scores:
            sum += score.popularity
        if len(scores) > 0:
            return sum / len(scores)
        else:
            return 0

    def get_value(self):
        sum = 0
        players = Player.objects.filter(team=self)
        for player in players:
            sum += player.market_value
        return sum


class Referee(models.Model):
    name = models.CharField(max_length=50)
    nationality = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='referees')
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)


class Match(models.Model):
    MATCH_STATUSES = (('NH', 'not held'),
                      ('OG', 'ongoing'),
                      ('H', 'held'),)
    host_team = models.ForeignKey(Team, on_delete=models.RESTRICT, related_name='host_team_match')
    guest_team = models.ForeignKey(Team, on_delete=models.RESTRICT, related_name='guest_team_match')
    host_team_goal_count = models.IntegerField()
    guest_team_goal_count = models.IntegerField()
    time = models.DateTimeField()
    tournament_season = models.ForeignKey(TournamentSeason, on_delete=models.RESTRICT, related_name='matches')
    status = models.CharField(max_length=10, choices=MATCH_STATUSES)
    round = models.CharField(max_length=20)
    stadium = models.ForeignKey(Stadium, on_delete=models.RESTRICT, related_name='matches')
    main_referee = models.ForeignKey(Referee, on_delete=models.RESTRICT, related_name='matches')
    assist_referees = models.ManyToManyField(Referee)


class Player(models.Model):
    FOOT = (('L', 'Left'),
            ('R', 'Right'))
    POSTS = (('GK', 'GoalKeeper'),
             ('RB', 'Right Back'),
             ('CB', 'Center Back'),
             ('LB', 'Left Back'),
             ('CM', 'Center Midfielder'),
             ('RM', 'Right Midfielder'),
             ('LM', 'Left Midfielder'),
             ('LW', 'Left Winger'),
             ('RW', 'Right Winger'),
             ('ST', 'Striker'))
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    desc = models.TextField(max_length=500)
    nationality = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='players')
    main_foot = models.CharField(max_length=6, null=True, blank=True, choices=FOOT)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    post = models.CharField(max_length=20, choices=POSTS)
    # market_value = models.DecimalField(max_digits=9, decimal_places=2)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)
    birth_date = models.DateField()

    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year

    # def get_value
    def __str__(self):
        return self.name


class Goal(models.Model):
    AREAS = (('LF', 'left foot'),
             ('RF', 'right foot'),
             ('H', 'head'),
             ('O', 'other'))
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='goals')
    scorer = models.ForeignKey(Player, on_delete=models.RESTRICT, related_name='goal_by_player')
    assist_by = models.ForeignKey(Player, on_delete=models.RESTRICT, related_name='goal_assisted_by_player', blank=True,
                                  null=True)
    time = models.CharField(max_length=10)
    body_area = models.CharField(max_length=15, choices=AREAS)
    is_og = models.BooleanField(default=False)


class Booking(models.Model):
    CARDS = (('R', 'red'),
             ('Y', 'yellow'))
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bookings')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='bookings')
    time = models.CharField(max_length=10)
    card = models.CharField(max_length=10, choices=CARDS)


class Substitutions(models.Model):
    time = models.CharField(max_length=10)
    in_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='in_subs')
    out_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='out_subs')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='subs')


class PLayerMatchStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_match_stats')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='player_match_stats')
    saves = models.IntegerField(default=0)
    passes = models.IntegerField(default=0)
    complete_passes = models.IntegerField(default=0)
    dribbles = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    interceptions = models.IntegerField(default=0)
    key_passes = models.IntegerField(default=0)
    shots = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    shot_percentage = models.IntegerField()
    # the fields below should be saved using queries on other tables
    complete_pass_percentage = models.IntegerField()
    own_goals = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    score = models.IntegerField(default=5)


class TeamMatchStats(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_match_stats')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='team_match_stats')
    possession = models.IntegerField()
    corners = models.IntegerField(default=0)
    offsides = models.IntegerField(default=0)
    # the fields below should be saved using queries on other tables
    shots = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    shot_percentage = models.IntegerField()
    goals = models.IntegerField(default=0)
    complete_pass_percentage = models.IntegerField()


class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    former_club = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='out_transfers')
    destination_club = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='in_transfers')
    date = models.DateField()
    cost = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return '{0} from {1} to {2}'.format(self.player.name, self.former_club.name, self.destination_club.name)


class Popularities(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    popularity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = (('user', 'team'),)
        index_together = (('user', 'team'),)
