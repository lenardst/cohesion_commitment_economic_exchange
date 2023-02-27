from os import environ

SESSION_CONFIGS = [
     dict(
         name='EcoEx_RS',
         display_name="Economic Exchange and Reputation Systems (Treatment)",
         app_sequence=['instruction', 'negotiation', 'scmeasure'],
         num_demo_participants=6,
         rs=True
     ),
    dict(
        name='EcoEx_NoRS_25',
         display_name="Economic Exchange and Reputation Systems (Baseline, 25 rounds)",
         app_sequence=['instruction', 'negotiation25', 'scmeasure'],
         num_demo_participants=6,
         rs=False),
    dict(
        name='EcoEx_NoRS_26',
        display_name="Economic Exchange and Reputation Systems (Baseline, 26 rounds)",
        app_sequence=['instruction', 'negotiation26', 'scmeasure'],
        num_demo_participants=6,
        rs=False)
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['exchange_list', 'player_order', 'player_colors']
SESSION_FIELDS = []

# ROOMS
ROOMS = [
    dict(
        name='RoomT',
        use_secure_urls=False,
        display_name='RoomT',
        participant_label_file='_rooms/roomT.txt'
    ),
    dict(
        name='roomB',
        use_secure_urls=False,
        display_name='RoomB',
        participant_label_file='_rooms/roomT.txt'
    ),
    dict(
        name='roomR',
        use_secure_urls=False,
        display_name='RoomR',
        participant_label_file='_rooms/roomT.txt'
    )
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1981014152298'
