from otree.api import *
import os
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
import time
import random

from .models import C, Subsession, Group, Player

class Introduction(Page):
    form_model = 'player'

    def is_displayed(self):
        return not self.player.attention_failed

    def vars_for_template(self):
        # Wenn noch keine Startzeit gespeichert ist, speichern
        if 'start_time' not in self.player.participant.vars:
            self.player.participant.vars['start_time'] = time.time()
        return {}

class PreQuestionnaire(Page):
    form_model = 'player'
    #Questions from questionnaire of „Kim, J., Hong, L., and Evans, S. 2024. “Toward measuring data literacy for higher education: Developing
                                     #and validating a data literacy self-efficacy scale,” Journal of the Association for Information Science and Technology (75:8), pp. 916–931.“
    form_fields = [
    'data_attention_2','DLSE_DI1', 'DLSE_DI2', 'DLSE_DI3', 'DLSE_DI4', 'DLSE_DI5', 'DLSE_DI6', 'DLSE_DI7',
    'DLSE_DP1', 'DLSE_DP2', 'DLSE_DP3', 'DLSE_DP4', 'DLSE_DP5',
    'DLSE_DP6', 'DLSE_DP7', 'DLSE_DP8', 'DLSE_DP9', 'DLSE_DP10',
    'DLSE_DP11', 'DLSE_DP12', 'DLSE_DP13', 'DLSE_DP14', 'DLSE_DP15', 'DLSE_DP16',
    'DLSE_DMS1', 'DLSE_DMS2', 'DLSE_DMS3', 'DLSE_DMS4',
    'DLSE_DMS5', 'DLSE_DMS6', 'DLSE_DMS7', 'DLSE_DMS8'
    ]

    def vars_for_template(self):
        
        return dict(reversed_choices=C.LIKERT_CHOICES)
            
            
    def get_form_fields(self):
        fields = self.form_fields.copy()
        random.shuffle(fields)
        return fields

    def before_next_page(self):
        attention_checks = {
            'data_attention_2': 1
        }

        for field, should_be_true in attention_checks.items():
            if getattr(self.player, field) != should_be_true:
                self.player.attention_failed = True

class Intro(Page):
    form_model = 'player'

    def is_displayed(self):
        return not self.player.attention_failed

    def vars_for_template(self):
            return dict(treatment=self.player.treatment, base=self.session.config['participation_fee'], additional=self.session.config['real_world_currency_per_point'] )


class TreatmentA_easy(Page):
    form_model = 'player'
    form_fields = ['manipulation_check', 'tool_easy_checkout', 'tool_easy_problem1', 'data_attention_3', 'tool_easy_problem2']
    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'A' and not self.player.attention_failed

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

        attention_checks = {
            'data_attention_3': 'third',
        }

        #normal questions
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score += score

        #attention checks
        for field, should_be_true in attention_checks.items():
            if getattr(self.player, field) != should_be_true:
                self.player.attention_failed = True


class TreatmentB_easy(Page):
    form_model = 'player'
    form_fields = ['manipulation_check', 'excel_easy_problem1', 'data_attention_7', 'excel_easy_problem2', 'excel_easy_problem4']
    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'B'and not self.player.attention_failed

    def vars_for_template(self):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA_EASY.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)

    def before_next_page(self):
        correct_answers = {
            'excel_easy_problem1': 'C',
            'excel_easy_problem2': 'assignment',
            'excel_easy_problem4': 'pivot'
        }

        attention_checks = {
            'data_attention_7': 'rows',
        }

        #normal questions
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score += score

        #attention checks
        for field, should_be_true in attention_checks.items():
            if getattr(self.player, field) != should_be_true:
                self.player.attention_failed = True

class TreatmentA_difficult(Page):
    form_model = 'player'
    form_fields = [
        'tool_difficult_problem1', 'tool_difficult_problem2',
        'tool_difficult_steps1', 'tool_difficult_steps2', 'tool_difficult_steps3', 'tool_difficult_steps4', 'tool_difficult_steps5',
        'data_attention_5', 'tool_difficult_col1'
    ]

    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'A' and not self.player.attention_failed

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

        attention_checks = {
            'data_attention_5': 'third'
        }

        #normal questions
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score += score

        #attention checks
        for field, should_be_true in attention_checks.items():
            if getattr(self.player, field) != should_be_true:
                self.player.attention_failed = True





class TreatmentB_difficult(Page):
    form_model = 'player'
    form_fields = ['excel_difficult_problem1', 'excel_difficult_problem2',
                   'excel_difficult_steps1',  'excel_difficult_steps2',  'excel_difficult_steps3',  'excel_difficult_steps4',  'excel_difficult_steps5',
                    'excel_difficult_col1', 'data_attention_6']
    timeout_seconds = 600  # TODO hier 8 Minuten einstellen

    def is_displayed(self):
        return self.player.treatment == 'B' and not self.player.attention_failed

    def vars_for_template(self):
        # Erste Zeile aus Excel als Beispiel
        ausschnitt = C.DATA_DIFFICULT.head(5).to_html(index=False)
        return dict(aufgabe=ausschnitt)
    
    def before_next_page(self):
        correct_answers = {
            'excel_difficult_problem1': 'invalid characters', 
            'excel_difficult_problem2': 'missing col names', 
            'excel_difficult_steps1': False,
            'excel_difficult_steps2': True,
            'excel_difficult_steps3': False,
            'excel_difficult_steps4': True,
            'excel_difficult_steps5': False,
            'excel_difficult_col1': 'city'
        }

        attention_checks = {
            'data_attention_6': 'third'
        }

        #normal questions
        score = 0
        for field, should_be_true in correct_answers.items():
            if getattr(self.player, field) == should_be_true:
                score += 1
        self.player.score += score

        #attention checks
        for field, should_be_true in attention_checks.items():
            if getattr(self.player, field) != should_be_true:
                self.player.attention_failed = True

class TimeUp(Page):
    form_model = 'player'
    timeout_seconds = 25 # TODO hier 30 Sekunden einstellen

class PostQuestionnaire(Page):
    form_model = 'player'

    def is_displayed(self):
        return not self.player.attention_failed

    def get_form_fields(self):
        if self.player.treatment == 'A':
            return ['post_experience', 'difficulties', 'satisfaction','prolificID', 'age', 'gender', 'employment_status', 'job_type', 'education']
        else:
            return ['difficulties','prolificID', 'age', 'gender', 'employment_status', 'job_type', 'education']

class ThankYou(Page):
    form_model = 'player'

    def is_displayed(self):
        return not self.player.attention_failed


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

class Failure(Page):
    def is_displayed(self):
        return self.player.attention_failed

page_sequence = [
    Introduction,
    PreQuestionnaire,
    Intro,
    TreatmentA_easy,
    TreatmentB_easy,
    #TimeUp,
    TreatmentA_difficult,
    TreatmentB_difficult,
    Failure,
    PostQuestionnaire,
    ThankYou
    ]