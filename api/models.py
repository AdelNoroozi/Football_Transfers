from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

class Team(models.Model):
    LEAGUE = (
        ('SA', 'Serie A'),
        ('LFP', 'Laliga'),
        ('BL', 'Bundesliga'),
        ('L1', 'League 1'),
        ('EPL', 'Premiere League')
    )
    name = models.CharField(max_length=20)
    desc = models.TextField(max_length=500)
    league = models.CharField(max_length=20, choices=LEAGUE)
    market_value = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    president = models.CharField(max_length=50)
    open_transfer_window = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

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


class Player(models.Model):
    COUNTRIES = (
        ('AF', 'AFGHANISTAN'),
        ('AL', 'ALBANIA'),
        ('DZ', 'ALGERIA'),
        ('AS', 'AMERICAN SAMOA'),
        ('AD', 'ANDORRA'),
        ('AO', 'ANGOLA'),
        ('AI', 'ANGUILLA'),
        ('AQ', 'ANTARCTICA'),
        ('AG', 'ANTIGUA AND BARBUDA'),
        ('AR', 'ARGENTINA'),
        ('AM', 'ARMENIA'),
        ('AW', 'ARUBA'),
        ('AU', 'AUSTRALIA'),
        ('AT', 'AUSTRIA'),
        ('AZ', 'AZERBAIJAN'),
        ('BS', 'BAHAMAS'),
        ('BH', 'BAHRAIN'),
        ('BD', 'BANGLADESH'),
        ('BB', 'BARBADOS'),
        ('BY', 'BELARUS'),
        ('BE', 'BELGIUM'),
        ('BZ', 'BELIZE'),
        ('BJ', 'BENIN'),
        ('BM', 'BERMUDA'),
        ('BT', 'BHUTAN'),
        ('BO', 'BOLIVIA'),
        ('BA', 'BOSNIA AND HERZEGOVINA'),
        ('BW', 'BOTSWANA'),
        ('BV', 'BOUVET ISLAND'),
        ('BR', 'BRAZIL'),
        ('IO', 'BRITISH INDIAN OCEAN TERRITORY'),
        ('BN', 'BRUNEI DARUSSALAM'),
        ('BG', 'BULGARIA'),
        ('BF', 'BURKINA FASO'),
        ('BI', 'BURUNDI'),
        ('KH', 'CAMBODIA'),
        ('CM', 'CAMEROON'),
        ('CA', 'CANADA'),
        ('CV', 'CAPE VERDE'),
        ('KY', 'CAYMAN ISLANDS'),
        ('CF', 'CENTRAL AFRICAN REPUBLIC'),
        ('TD', 'CHAD'),
        ('CL', 'CHILE'),
        ('CN', 'CHINA'),
        ('CX', 'CHRISTMAS ISLAND'),
        ('CC', 'COCOS (KEELING) ISLANDS'),
        ('CO', 'COLOMBIA'),
        ('KM', 'COMOROS'),
        ('CG', 'CONGO'),
        ('CD', 'CONGO, THE DEMOCRATIC REPUBLIC OF'),
        ('CK', 'COOK ISLANDS'),
        ('CR', 'COSTA RICA'),
        ('CI', "CÃ”TE D'IVOIRE"),
        ('HR', 'CROATIA'),
        ('CU', 'CUBA'),
        ('CY', 'CYPRUS'),
        ('CZ', 'CZECH REPUBLIC'),
        ('DK', 'DENMARK'),
        ('DJ', 'DJIBOUTI'),
        ('DM', 'DOMINICA'),
        ('DO', 'DOMINICAN REPUBLIC'),
        ('EC', 'ECUADOR'),
        ('EG', 'EGYPT'),
        ('SV', 'EL SALVADOR'),
        ('GQ', 'EQUATORIAL GUINEA'),
        ('ER', 'ERITREA'),
        ('EE', 'ESTONIA'),
        ('ET', 'ETHIOPIA'),
        ('FK', 'FALKLAND ISLANDS (MALVINAS)'),
        ('FO', 'FAROE ISLANDS'),
        ('FJ', 'FIJI'),
        ('FI', 'FINLAND'),
        ('FR', 'FRANCE'),
        ('GF', 'FRENCH GUIANA'),
        ('PF', 'FRENCH POLYNESIA'),
        ('TF', 'FRENCH SOUTHERN TERRITORIES'),
        ('GA', 'GABON'),
        ('GM', 'GAMBIA'),
        ('GE', 'GEORGIA'),
        ('DE', 'GERMANY'),
        ('GH', 'GHANA'),
        ('GI', 'GIBRALTAR'),
        ('GR', 'GREECE'),
        ('GL', 'GREENLAND'),
        ('GD', 'GRENADA'),
        ('GP', 'GUADELOUPE'),
        ('GU', 'GUAM'),
        ('GT', 'GUATEMALA'),
        ('GN', 'GUINEA'),
        ('GW', 'GUINEA'),
        ('GY', 'GUYANA'),
        ('HT', 'HAITI'),
        ('HM', 'HEARD ISLAND AND MCDONALD ISLANDS'),
        ('HN', 'HONDURAS'),
        ('HK', 'HONG KONG'),
        ('HU', 'HUNGARY'),
        ('IS', 'ICELAND'),
        ('IN', 'INDIA'),
        ('ID', 'INDONESIA'),
        ('IR', 'IRAN, ISLAMIC REPUBLIC OF'),
        ('IQ', 'IRAQ'),
        ('IE', 'IRELAND'),
        ('IL', 'ISRAEL'),
        ('IT', 'ITALY'),
        ('JM', 'JAMAICA'),
        ('JP', 'JAPAN'),
        ('JO', 'JORDAN'),
        ('KZ', 'KAZAKHSTAN'),
        ('KE', 'KENYA'),
        ('KI', 'KIRIBATI'),
        ('KP', "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF"),
        ('KR', 'KOREA, REPUBLIC OF'),
        ('KW', 'KUWAIT'),
        ('KG', 'KYRGYZSTAN'),
        ('LA', "LAO PEOPLE'S DEMOCRATIC REPUBLIC"),
        ('LV', 'LATVIA'),
        ('LB', 'LEBANON'),
        ('LS', 'LESOTHO'),
        ('LR', 'LIBERIA'),
        ('LY', 'LIBYAN ARAB JAMAHIRIYA'),
        ('LI', 'LIECHTENSTEIN'),
        ('LT', 'LITHUANIA'),
        ('LU', 'LUXEMBOURG'),
        ('MO', 'MACAO'),
        ('MK', 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF'),
        ('MG', 'MADAGASCAR'),
        ('MW', 'MALAWI'),
        ('MY', 'MALAYSIA'),
        ('MV', 'MALDIVES'),
        ('ML', 'MALI'),
        ('MT', 'MALTA'),
        ('MH', 'MARSHALL ISLANDS'),
        ('MQ', 'MARTINIQUE'),
        ('MR', 'MAURITANIA'),
        ('MU', 'MAURITIUS'),
        ('YT', 'MAYOTTE'),
        ('MX', 'MEXICO'),
        ('FM', 'MICRONESIA, FEDERATED STATES OF'),
        ('MD', 'MOLDOVA, REPUBLIC OF'),
        ('MC', 'MONACO'),
        ('MN', 'MONGOLIA'),
        ('MS', 'MONTSERRAT'),
        ('MA', 'MOROCCO'),
        ('MZ', 'MOZAMBIQUE'),
        ('MM', 'MYANMAR'),
        ('NA', 'NAMIBIA'),
        ('NR', 'NAURU'),
        ('NP', 'NEPAL'),
        ('NL', 'NETHERLANDS'),
        ('AN', 'NETHERLANDS ANTILLES'),
        ('NC', 'NEW CALEDONIA'),
        ('NZ', 'NEW ZEALAND'),
        ('NI', 'NICARAGUA'),
        ('NE', 'NIGER'),
        ('NG', 'NIGERIA'),
        ('NU', 'NIUE'),
        ('NF', 'NORFOLK ISLAND'),
        ('MP', 'NORTHERN MARIANA ISLANDS'),
        ('NO', 'NORWAY'),
        ('OM', 'OMAN'),
        ('PK', 'PAKISTAN'),
        ('PW', 'PALAU'),
        ('PS', 'PALESTINIAN TERRITORY, OCCUPIED'),
        ('PA', 'PANAMA'),
        ('PG', 'PAPUA NEW GUINEA'),
        ('PY', 'PARAGUAY'),
        ('PE', 'PERU'),
        ('PH', 'PHILIPPINES'),
        ('PN', 'PITCAIRN'),
        ('PL', 'POLAND'),
        ('PT', 'PORTUGAL'),
        ('PR', 'PUERTO RICO'),
        ('QA', 'QATAR'),
        ('RE', 'RÃ‰UNION'),
        ('RO', 'ROMANIA'),
        ('RU', 'RUSSIAN FEDERATION'),
        ('RW', 'RWANDA'),
        ('SH', 'SAINT HELENA'),
        ('KN', 'SAINT KITTS AND NEVIS'),
        ('LC', 'SAINT LUCIA'),
        ('PM', 'SAINT PIERRE AND MIQUELON'),
        ('VC', 'SAINT VINCENT AND THE GRENADINES'),
        ('WS', 'SAMOA'),
        ('SM', 'SAN MARINO'),
        ('ST', 'SAO TOME AND PRINCIPE'),
        ('SA', 'SAUDI ARABIA'),
        ('SN', 'SENEGAL'),
        ('CS', 'SERBIA AND MONTENEGRO'),
        ('SC', 'SEYCHELLES'),
        ('SL', 'SIERRA LEONE'),
        ('SG', 'SINGAPORE'),
        ('SK', 'SLOVAKIA'),
        ('SI', 'SLOVENIA'),
        ('SB', 'SOLOMON ISLANDS'),
        ('SO', 'SOMALIA'),
        ('ZA', 'SOUTH AFRICA'),
        ('GS', 'SOUTH GEORGIA AND SOUTH SANDWICH ISLANDS'),
        ('ES', 'SPAIN'),
        ('LK', 'SRI LANKA'),
        ('SD', 'SUDAN'),
        ('SR', 'SURINAME'),
        ('SJ', 'SVALBARD AND JAN MAYEN'),
        ('SZ', 'SWAZILAND'),
        ('SE', 'SWEDEN'),
        ('CH', 'SWITZERLAND'),
        ('SY', 'SYRIAN ARAB REPUBLIC'),
        ('TW', 'TAIWAN, PROVINCE OF CHINA'),
        ('TJ', 'TAJIKISTAN'),
        ('TZ', 'TANZANIA, UNITED REPUBLIC OF'),
        ('TH', 'THAILAND'),
        ('TL', 'TIMOR'),
        ('TG', 'TOGO'),
        ('TK', 'TOKELAU'),
        ('TO', 'TONGA'),
        ('TT', 'TRINIDAD AND TOBAGO'),
        ('TN', 'TUNISIA'),
        ('TR', 'TURKEY'),
        ('TM', 'TURKMENISTAN'),
        ('TC', 'TURKS AND CAICOS ISLANDS'),
        ('TV', 'TUVALU'),
        ('UG', 'UGANDA'),
        ('UA', 'UKRAINE'),
        ('AE', 'UNITED ARAB EMIRATES'),
        ('GB', 'UNITED KINGDOM'),
        ('US', 'UNITED STATES'),
        ('UM', 'UNITED STATES MINOR OUTLYING ISLANDS'),
        ('UY', 'URUGUAY'),
        ('UZ', 'UZBEKISTAN'),
        ('VU', 'VANUATU'),
        ('VN', 'VIET NAM'),
        ('VG', 'VIRGIN ISLANDS, BRITISH'),
        ('VI', 'VIRGIN ISLANDS, U.S.'),
        ('WF', 'WALLIS AND FUTUNA'),
        ('EH', 'WESTERN SAHARA'),
        ('YE', 'YEMEN'),
        ('ZW', 'ZIMBABWE')
    )
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
    desc = models.TextField(max_length=500)
    nationality = models.CharField(max_length=20, choices=COUNTRIES)
    main_foot = models.CharField(max_length=6, null=True, blank=True, choices=FOOT)
    age = models.IntegerField(validators=[
        MaxValueValidator(60),
        MinValueValidator(15)
    ])
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    post = models.CharField(max_length=20, choices=POSTS)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)

    def __str__(self):
        return self.name


class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    former_club = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='former')
    destination_club = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='dest')
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
