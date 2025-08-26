import random
import time
from otree.api import *
from pathlib import Path
import pandas as pd
from django.utils.safestring import mark_safe

class C(BaseConstants):
    NAME_IN_URL = 'th1nk_app'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TREATMENT = ['A', 'B']
    EXCEL_FILE_DIFFICULT = EXCEL_FILE_DIFFICULT = Path(__file__).parent / 'static' / 'data' / 'dataset_difficult.xlsx'
    DATA_DIFFICULT = pd.read_excel(EXCEL_FILE_DIFFICULT)
    EXCEL_FILE_EASY = EXCEL_FILE_EASY = Path(__file__).parent / 'static' / 'data' / 'dataset_easy.xlsx'
    DATA_EASY = pd.read_excel(EXCEL_FILE_EASY)

class Subsession(BaseSubsession):
    def creating_session(self):
        #import itertools
        #TREATMENT = itertools.cycle(['A', 'B'])
        for p in self.get_players():
            p.treatment = random.choice(C.TREATMENT)

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treatment = models.StringField()

    # Introduction
    prolificID = models.IntegerField(label='Prolific ID')
    age = models.IntegerField(label='Age')
    gender = models.StringField(
        choices=['male', 'female', 'diverse'],
        label='Gender'
    )
    employment_status = models.StringField(
        choices=['Permenant employee', 'Temporary employee', 'Casual employee', 'Student', 'Intern', 'Consultant'],
        label='What is your employment status?'
    )
    job_type = models.StringField(
        choices=['Technical', 'Professional', 'Management'],
        label='What is your job type?'
    )
    education = models.StringField(
        choices=['Diploma below college level', 'College diploma', 'University degree below baccalaureate', 'Bachelor\'s degree', 'Master\'s degree', 'Ph.D. or higher degree'],
        label='What is the highest level of education that you have completed?'
    )

    # Pre-questionnaire
    data_conversion = models.StringField(
        label="Data conversion (modifying the format in which the data is stored in order to make it more usable)",
        choices=["I know the tools and practices used in data conversion.", "I understand the impacts that converting data may have on its use.", "I'm capable of converting data in order to increase its use value.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )
    data_cleansing = models.StringField(
        label="Data cleansing (modifying data in order to reduce any errors which could affect quality)",
        choices=["I know the tools and practices used in data cleansing.", "I understand the effects and limits that data cleansing may have on its ability to be used.", "I'm capable of converting data in order to increase its use value.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )
    data_transformation = models.StringField(
        label="Data transformation (organizing, structuring, compiling and aggregating data in order to aid in analysis and decision making)",
        choices=["I know the tools and practices used in data transformation.", "I understand the methods used in data transformation and the consequences of using different tools and practices.", "I'm capable of transforming data in order to increase its value for analysis and decision making.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )
    data_metadata = models.StringField(
        label="Creating business metadata (adding information to data, in particular to document any transformation, in order to aid in data classification, sharing and reuse)",
        choices=["I understand the concept of business metadata.", "I understand the concept of metadata and its use in contextualizing data.", "I'm capable of creating business metadata in order to aid in data classification, sharing and reuse.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )
    data_visualization = models.StringField(
         label="Creating data visualizations (creating graphical representations in order to communicate the significance of data)",
         choices=["I understand the different types of data visualizations.", "I understand the consequences that the choice of data visualization has on its ability to be communicated.", "I'm capable of creating graphical representations which communicate the significance of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
         widget=widgets.RadioSelect
    )
    data_interactive = models.StringField(
         label="Interactive data querying (progressively understanding the significance of data by using interactive analysis to derive an explanation of the reality it represents)",
         choices=["I understand the methods and tools used to interactively query data.", "I understand the possibilities and limits of interactive data queries.", "I'm capable of interactively querying data in order to understand its significance.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
         widget=widgets.RadioSelect
    )
    data_interpretation = models.StringField(
         label="Data interpretation (interpreting data in order to understand its significance and derive and explanation of the reality it represents)",
         choices=["I understand the methods and tools used to interpret data.", "I understand how interpreting data can explain reality.", "I'm capable of interpreting data in order to understand its significance.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
         widget=widgets.RadioSelect
    )
    data_communication = models.StringField(
        label="Communicating the significance of data (sharing the significance of data with other people, verbally or in writing)",
        choices=["I understand the practices used to share the significance of data.", "I understand the effects of using good practices to communicate the significance of data.", "I'm capable of communicating the significance of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )

#Treatment
#easy

    tool_easy_checkout = models.StringField(choices= [
        mark_safe('<img src="/static/data/false_1.png" width="100">'),
        mark_safe('<img src="/static/data/false_2.png" width="100">'),
        mark_safe('<img src="/static/data/correct.png" width="100">'),
        mark_safe('<img src="/static/data/false_3.png" width="100">')
        ],
        label='How does the result columns look like?',
        widget=widgets.RadioSelect
    )

    tool_easy_problem1 = models.StringField(choices= [
        'The values are not properly formatted.',
        'The values depend on multiple attributes that are not clearly structured.',
        'The structure is not normalized.',
        'The structure is flat and clean, but the cells contents too much information.'
        ],
        label='Why is the nested structure of the dataset problematic?',
        widget=widgets.RadioSelect
    )

    tool_easy_problem2 = models.StringField(choices= [
        'The structure got more complex.',
        'The attributes now extend over only one column.',
        'Many duplicates were created.',
        'The data format has changed.'
        ],
        label='What has changed in the transformation process?',
        widget=widgets.RadioSelect
    )

#difficult
    # Post-questionnaire
    post_experience = models.LongStringField(
        label="Please describe your experience using the tool.",
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
    #uploaded_filename = models.StringField(blank=True)
