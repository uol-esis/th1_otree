from otree.api import *
import os
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
import time

from .models import C, Subsession, Group, Player

class Introduction(Page):
    form_model = 'player'
    form_fields = ['prolificID', 'age', 'gender', 'employment_status', 'job_type', 'education']

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
        'data_attention_1',
        'data_interactive',
        'data_attention_2',
        'data_interpretation',
        'data_communication',
        ]

class Intro(Page):
    form_model = 'player'

class TreatmentA_easy(Page):
    form_model = 'player'
    form_fields = ['tool_easy_checkout', 'tool_easy_problem1', 'data_attention_3', 'tool_easy_problem2']
    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'A'

    def vars_for_template(self):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA_EASY.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)
    
    def before_next_page(self):
        correct_answers = {
            'tool_easy_checkout': 'C',
            'tool_easy_problem1': 'multiple attributes',
            'tool_easy_problem2': 'one col attributes'
        }
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score += score


class TreatmentB_easy(Page):
    form_model = 'player'
    form_fields = ['excel_easy_problem1', 'data_attention_7', 'excel_easy_problem2', 'excel_easy_problem3', 'excel_easy_problem4']
    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'B'

    def vars_for_template(self):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA_EASY.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)

    def before_next_page(self):
        correct_answers = {
            'excel_easy_problem1': 'C',
            'excel_easy_problem2': 'assignment',
            'excel_easy_problem3': 'gender_age',
            'excel_easy_problem4': 'pivot'
        }
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score += score

class TreatmentA_difficult(Page):
    form_model = 'player'
    form_fields = [
        'tool_difficult_problem1', 'tool_difficult_problem2',
        'tool_difficult_steps1', 'tool_difficult_steps2', 'tool_difficult_steps3', 'data_attention_5', 'tool_difficult_steps4', 'tool_difficult_steps5',
        'tool_difficult_col1', 'data_attention_4'
    ]

    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'A'

    def vars_for_template(self):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA_DIFFICULT.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)
    
    def before_next_page(self):
        correct_answers = {
            'tool_difficult_problem1': 'invalid characters',
            'tool_difficult_problem2': 'missing col names',
            'tool_difficult_steps1' : False, 'tool_difficult_steps2' : True, 'tool_difficult_steps3': True, 'tool_difficult_steps4': False, 'tool_difficult_steps5': True,
            'tool_difficult_col1': 'city'
        }
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score += score

        


class TreatmentB_difficult(Page):
    form_model = 'player'
    form_fields = ['excel_difficult_problem1', 'excel_difficult_problem2',
                   'excel_difficult_steps1',  'excel_difficult_steps2',  'excel_difficult_steps3',  'excel_difficult_steps4',  'excel_difficult_steps5',
                    'excel_difficult_col1', 'data_attention_6']
    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'B'

    def vars_for_template(self):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA_DIFFICULT.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)
    
    def before_next_page(self):
        correct_answers = {
            'excel_difficult_problem1': 'invalid characters', 
            'excel_difficult_problem2': 'missing col names', 
            'excel_difficult_steps1': False,
            'excel_difficult_steps1': True,
            'excel_difficult_steps1': False,
            'excel_difficult_steps1': True,
            'excel_difficult_steps1': False,
            'excel_difficult_col1': 'city'
        }
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score += score

class TimeUp(Page):
    form_model = 'player'
    timeout_seconds = 25 # TODO hier 30 Sekunden einstellen

class PostQuestionnaire(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.player.treatment == 'A':
            return ['post_experience', 'difficulties', 'satisfaction']
        else:
            return ['difficulties', 'satisfaction']

class ThankYou(Page):
    form_model = 'player'

    def vars_for_template(self):
            end_time = time.time()
            start_time = self.player.participant.vars.get('start_time', end_time)
            total_duration = end_time - start_time  # Zeit in Sekunden
            self.player.participant.vars['total_duration'] = total_duration
            score_bonus = self.player.score * self.session.config['real_world_currency_per_point']
            self.player.payoff = cu(score_bonus)
            payoff_exact = self.session.config['participation_fee'] + float(self.player.payoff)
            return dict(
                payoff_exact=round(payoff_exact, 2),  # auf 2 Nachkommastellen
                score=self.player.score,
                total_duration=self.player.participant.vars.get('total_duration', 0)
            )

page_sequence = [
    Introduction,
    PreQuestionnaire,
    Intro,
    TreatmentA_easy,
    TreatmentB_easy,
    #TimeUp,
    TreatmentA_difficult,
    TreatmentB_difficult,
    PostQuestionnaire,
    ThankYou
    ]