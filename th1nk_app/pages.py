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

class TreatmentB(Page):
    def is_displayed(self):
        form_fields = ['B']
        return self.treatment == 'B'

class Intro(Page):
    form_model = 'player'
    timeout_seconds = 2  # TODO hier sollten ca 2 Minuten eingestellt werden -> fürs testen nur verkürzte zeit

class TreatmentA_easy(Page):
    form_model = 'player'
    form_fields = ['mc1', 'mc2', 'mc3', 'open1', 'open2', 'open3']
    timeout_seconds = 5  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'A'
        #return self.player.TREATMENT == 'A'

    def vars_for_template(player):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)

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

    def before_next_page(self, timeout_happened):
        # Automatische Auswertung Multiple Choice
        correct_answers = {'mc1': 'A', 'mc2': 'B', 'mc3': 'C'}
        score = sum(getattr(player, q) == ans for q, ans in correct_answers.items())
        self.score_mc = score

        # Beispiel für offene Fragen – hier nur Länge der Antwort > 0 als "korrekt"
        open_score = sum(len(getattr(self, q) or '') > 0 for q in ['open1', 'open2', 'open3'])
        self.score_open = open_score

        if timeout_happened:
            self.participant.vars['timeout_reached'] = True
        else:
            self.participant.vars['timeout_reached'] = False


class TimeUp(Page):
    form_model = 'player'
    timeout_seconds = 15 # TODO hier 30 Sekunden einstellen

class PostQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['post_experience', 'difficulties', 'satisfaction']

page_sequence = [
    #Introduction,
    #PreQuestionnaire,
    Intro,
    TreatmentA_easy,
    #TreatmentB_easy,
    TimeUp,
    #TreatmentA_difficult,
    #TreatmentB_difficult,
    PostQuestionnaire
    ]