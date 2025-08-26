from otree.api import *
import os
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
import time

from .models import C, Subsession, Group, Player

class Introduction(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'prolificID', 'employment_status', 'job_type', 'education']

    def vars_for_template(self):
        # Wenn noch keine Startzeit gespeichert ist, speichern
        if 'start_time' not in self.player.participant.vars:
            self.player.participant.vars['start_time'] = time.time()
        return {}

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

class TreatmentB_difficult(Page):
    form_model = 'player'
    form_fields = ['mc1', 'mc2', 'mc3', 'open1', 'open2', 'open3']
    timeout_seconds = 30  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'B'

    def vars_for_template(self):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)
    
    

class Intro(Page):
    form_model = 'player'

class TreatmentA_difficult(Page):
    form_model = 'player'
    form_fields = [
        'tool_difficult_problem1', 'tool_difficult_problem2',
        'bool_steps1', 'bool_steps2', 'bool_steps3', 'bool_steps4', 'bool_steps5',
        'tool_difficult_col1'
    ]
    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'A'

    def vars_for_template(self):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)
    
    #check if all correct awnsers are selected
    def before_next_page(self):
        correct_answers = {
            'tool_difficult_problem1': 'invalid characters',
            'tool_difficult_problem2': 'missing col names',
            'bool_steps1' : False, 'bool_steps2' : True, 'bool_steps3': True, 'bool_steps4': False, 'bool_steps5': True,
            'tool_difficult_col1': 'city'
        }
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score = score

        end_time = time.time()
        start_time = self.player.participant.vars.get('start_time', end_time)
        total_duration = end_time - start_time  # Zeit in Sekunden
        self.player.participant.vars['total_duration'] = total_duration

        base_pay = 1
        score_bonus = self.player.score * 0.1
        time_penalty = (total_duration / 60) * 0.1  # z.B. 0.10 pro Minute
        payoff_value = base_pay + score_bonus - time_penalty 
        print(payoff_value)
        self.player.payoff = cu(payoff_value)

    '''
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
'''

class ResultDifficultA(Page):
    form_model = 'player'
    
    def vars_for_template(self):
        payoff_exact = float(self.player.payoff)
        return dict(
            payoff_exact=round(payoff_exact, 2),  # auf 2 Nachkommastellen
            score=self.player.score,
            total_duration=self.player.participant.vars.get('total_duration', 0)
        )

class TimeUp(Page):
    form_model = 'player'
    timeout_seconds = 25 # TODO hier 30 Sekunden einstellen

class PostQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['post_experience', 'difficulties', 'satisfaction']

class ThankYou(Page):
    form_model = 'player'

page_sequence = [
    Introduction,
    #PreQuestionnaire,
    Intro,
    #TreatmentA_easy,
    #TreatmentB_easy,
    #TimeUp,
    TreatmentA_difficult,
    ResultDifficultA,
    TreatmentB_difficult,
    PostQuestionnaire,
    ThankYou
    ]