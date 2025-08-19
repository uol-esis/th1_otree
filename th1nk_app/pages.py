from otree.api import *
import os
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
import time

from .models import C, Subsession, Group, Player

class Introduction(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'prolificID', 'employment_status', 'job_type', 'education']

class PreQuestionnaire(Page):
    form_model = 'player'
    #Questions from questionnaire of LanglaisMosconiGuillemette
    form_fields = ['data_conversion',
        'data_cleansing',
        'data_transformation',
        'data_metadata',
        'data_visualization',
        'data_interactive',
        'data_interpretation',
        'data_communication',
        ]

'''class ToolAndUpload(Page):
    form_model = 'player'
    form_fields = []

    def vars_for_template(self):
        return {
            'external_url': f'https://yourtool.com/start?participant={self.participant.code}'
        }

    def post(self):
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        uploaded_file = self.request.POSTFILES.get('upload')
        if uploaded_file:
            filename = f"{self.participant.code}_{uploaded_file.name}"
            path = os.path.join('uploads', filename)
            default_storage.save(path, uploaded_file)
            self.player.uploaded_filename = filename
        return super().post()
'''

class SetTreatment(Page):
    def before_next_page(player, timeout_happened):
        player.treatment = player.subsession.get_treatment(player)

    @staticmethod
    def is_displayed(player):
        return False

class TreatmentA(Page):
    @staticmethod
    def is_displayed(player):
        form_fields = ['Treatment A']
        return player.treatment == 'A'

class TreatmentB(Page):
    @staticmethod
    def is_displayed(player):
        form_fields = ['Treatment B']
        return player.treatment == 'B'

class Intro(Page):
    form_model = 'player'
    timeout_seconds = 120  # 2 Minuten

    @staticmethod
    def vars_for_template(player):
        # Erste Zeile aus Excel als Beispiel
        aufgabe = C.DATA.iloc[0]['Aufgabe']
        return dict(aufgabe=aufgabe)

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Speichere Deadline für die 8 Minuten Bearbeitungszeit
        player.participant.vars['deadline'] = time.time() + (8 * 60)


class Questions(Page):
    form_model = 'player'
    form_fields = ['mc1', 'mc2', 'mc3', 'open1', 'open2', 'open3']

    @staticmethod
    def get_timeout_seconds(player):
        deadline = player.participant.vars.get('deadline')
        if deadline:
            remaining = deadline - time.time()
            return max(0, int(remaining))
        return None

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Automatische Auswertung Multiple Choice
        correct_answers = {'mc1': 'A', 'mc2': 'B', 'mc3': 'C'}
        score = sum(getattr(player, q) == ans for q, ans in correct_answers.items())
        player.score_mc = score

        # Beispiel für offene Fragen – hier nur Länge der Antwort > 0 als "korrekt"
        open_score = sum(len(getattr(player, q) or '') > 0 for q in ['open1', 'open2', 'open3'])
        player.score_open = open_score

        if timeout_happened:
            player.participant.vars['timeout_reached'] = True
        else:
            player.participant.vars['timeout_reached'] = False


class TimeUp(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.participant.vars.get('timeout_reached', False)

class SecondTaskIntro(Page):
    @staticmethod
    def is_displayed(player):
        return not player.participant.vars.get('timeout_reached', False)

#page_sequence = [TaskIntro, TaskQuestions, TimeUp, SecondTaskIntro]

class PostQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['post_experience', 'difficulties', 'satisfaction']

page_sequence = [
    Introduction,
    PreQuestionnaire,
    Intro,
    Questions,
    TimeUp,
    PostQuestionnaire
    ]