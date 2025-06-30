from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'th1nk_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Pre-questionnaire
    prior_knowledge = models.StringField(
        choices=["None", "Basic", "Intermediate", "Advanced"],
        widget=widgets.RadioSelect,
        label="What is your prior knowledge about this topic?"
    )
    motivation = models.StringField(
        label="What motivates you to participate?",
        blank=True
    )

    # Post-questionnaire
    post_experience = models.LongStringField(
        label="Describe your experience using the tool.",
        blank=True
    )
    difficulties = models.LongStringField(
        label="What difficulties did you encounter, if any?",
        blank=True
    )
    satisfaction = models.IntegerField(
        label="How satisfied are you with the tool?",
        choices=[[i, str(i)] for i in range(1, 6)],
        widget=widgets.RadioSelectHorizontal
    )

    # File tracking
    uploaded_filename = models.StringField(blank=True)
