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
        #A = Tool, B = Excel
        #TREATMENT = itertools.cycle(['A', 'B'])
        for p in self.get_players():
            #p.treatment = random.choice(C.TREATMENT)
            p.treatment = "A"

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treatment = models.StringField()
    score = models.IntegerField(initial=0)

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
        label="<h5> Data conversion (modifying the format in which the data is stored in order to make it more usable) </h5>",
        choices=["I know the tools and practices used in data conversion.", "I understand the impacts that converting data may have on its use.", "I'm capable of converting data in order to increase its use value.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )
    data_cleansing = models.StringField(
        label=" <h5> Data cleansing (modifying data in order to reduce any errors which could affect quality) </h5>",
        choices=["I know the tools and practices used in data cleansing.", "I understand the effects and limits that data cleansing may have on its ability to be used.", "I'm capable of converting data in order to increase its use value.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )
    data_transformation = models.StringField(
        label="<h5> Data transformation (organizing, structuring, compiling and aggregating data in order to aid in analysis and decision making) </h5>",
        choices=["I know the tools and practices used in data transformation.", "I understand the methods used in data transformation and the consequences of using different tools and practices.", "I'm capable of transforming data in order to increase its value for analysis and decision making.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )
    data_metadata = models.StringField(
        label="<h5> Creating business metadata (adding information to data, in particular to document any transformation, in order to aid in data classification, sharing and reuse) </h5>",
        choices=["I understand the concept of business metadata.", "I understand the concept of metadata and its use in contextualizing data.", "I'm capable of creating business metadata in order to aid in data classification, sharing and reuse.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )
    data_visualization = models.StringField(
         label= "<h5> Creating data visualizations (creating graphical representations in order to communicate the significance of data) </h5>",
         choices=["I understand the different types of data visualizations.", "I understand the consequences that the choice of data visualization has on its ability to be communicated.", "I'm capable of creating graphical representations which communicate the significance of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
         widget=widgets.RadioSelect
    )
    data_interactive = models.StringField(
         label="<h5> Interactive data querying (progressively understanding the significance of data by using interactive analysis to derive an explanation of the reality it represents) </h5>",
         choices=["I understand the methods and tools used to interactively query data.", "I understand the possibilities and limits of interactive data queries.", "I'm capable of interactively querying data in order to understand its significance.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
         widget=widgets.RadioSelect
    )
    data_interpretation = models.StringField(
         label="<h5> Data interpretation (interpreting data in order to understand its significance and derive and explanation of the reality it represents) </h5>",
         choices=["I understand the methods and tools used to interpret data.", "I understand how interpreting data can explain reality.", "I'm capable of interpreting data in order to understand its significance.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
         widget=widgets.RadioSelect
    )
    data_communication = models.StringField(
        label="<h5> Communicating the significance of data (sharing the significance of data with other people, verbally or in writing) </h5>",
        choices=["I understand the practices used to share the significance of data.", "I understand the effects of using good practices to communicate the significance of data.", "I'm capable of communicating the significance of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )

#Attention checks
    data_attention_1 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=["I understand the practices used to share the significance of data.", "I understand the effects of using good practices to communicate the meaning of data.", "I'm capable of understanding the background of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )

    data_attention_3 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=["I understand the practices used to share the significance of data.", "I understand the effects of using good practices to communicate the meaning of data.", "I'm capable of understanding the background of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )

    data_attention_4 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=["I understand the practices used to share the significance of data.", "I understand the effects of using good practices to communicate the meaning of data.", "I'm capable of understanding the background of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )

    data_attention_5 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=["I understand the practices used to share the significance of data.", "I understand the effects of using good practices to communicate the meaning of data.", "I'm capable of understanding the background of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )

    data_attention_6 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=["I understand the practices used to share the significance of data.", "I understand the effects of using good practices to communicate the meaning of data.", "I'm capable of understanding the background of data.", "My current work requires me to implement this skill.", "My current level in this skill is sufficient to carry out my work."],
        widget=widgets.RadioSelect
    )

    data_attention_2 = models.StringField(
            label="<h5> Which of the following is a common way to organize data? </h5>",
            choices=["By throwing papers randomly on the floor", "In rows and columns", "By using only your memory without writing anything down", "In drawn doodles on a napkin", "By singing the numbers out loud instead of writing them down"],
            widget=widgets.RadioSelect
    )

    data_attention_7 = models.StringField(
            label="<h5> Which of the following is a common way to organize data? </h5>",
            choices=["By throwing papers randomly on the floor", "In rows and columns", "By using only your memory without writing anything down", "In drawn doodles on a napkin", "By singing the numbers out loud instead of writing them down"],
            widget=widgets.RadioSelect
    )

#Treatment A
#easy
    tool_easy_checkout = models.StringField(choices= [
        ["A" ,mark_safe(' <img src="/static/data/false_1.png" width="400" style="margin:15px;"> ')],
        ["B",mark_safe(' <img src="/static/data/false_2.png" width="400" style="margin:15px;"> ')],
        ["C", mark_safe(' <img src="/static/data/correct.png" width="400" style="margin:15px;"> ')],
        ["D", mark_safe(' <img src="/static/data/false_3.png" width="400" style="margin:15px;" > ')],
        ],
        label='<h5> How does the result columns look like? </h5>',
        widget=widgets.RadioSelect
    )

    tool_easy_problem1 = models.StringField(choices= [
        ['false format', 'The values are not properly formatted.'],
        ['multiple attributes' , 'The values depend on multiple attributes that are not clearly structured.'],
        ['not normalized', 'The structure is not normalized.'],
        ['flat structure','The structure is flat and clean, but the cells contents too much information.']
        ],
        label='<h5> Why is the nested structure of the dataset problematic? </h5>',
        widget=widgets.RadioSelect
    )

    tool_easy_problem2 = models.StringField(choices= [
       ['complex structure' ,'The structure got more complex.'],
        ['one col attributes', 'The attributes now extend over only one column.'],
        ['duplicates', 'Many duplicates were created.'],
        ['changed format', 'The data format has changed.']
        ],
        label='<h5> What has changed in the transformation process? </h5>',
        widget=widgets.RadioSelect
    )

#difficult
    tool_difficult_problem1 = models.StringField(
        label="<h5> What problem areas do you identify in the raw data and how would you deal with these challenges in each case? </h5>",
        choices=[
           ["invalid characters" , "Invalid values: Replace special characters with appropriate values or remove them."],
           ["inconsistent spellings", "Inconsistent spellings in text categories: Standardize them using mapping or text normalization (lowercasing, removing special characters)."],
           ["missing values", "Missing values: Decide whether to fill in missing entries through imputation or remove rows with too many missing values."]
        ],
        widget=widgets.RadioSelect
    )

    tool_difficult_problem2 = models.StringField(
        label="<h5> What further problem areas do you identify? </h5>",
        choices=[["duplicates","Duplicates: Identify and remove duplicate entries to ensure data quality."],
            ["no problems", "Data is already completely clean and requires no further processing."],
           ["missing col names", "Missing column names: add to each column a unique name",]
        ],
        widget=widgets.RadioSelect
    )

    tool_difficult_steps1= models.BooleanField(
        label="<h5> Is the processing step <b>remove duplicates</b> necessary to prepare the data for analysis </h5>"
    )

    tool_difficult_steps2 = models.BooleanField(
        label="<h5>  Is the processing step <b>remove rows with invalid values</b> necessary to prepare the data for analysis </h5>"
    )
    tool_difficult_steps3 = models.BooleanField(
        label="<h5> Is the processing step <b>add column headers</b> necessary to prepare the data for analysis </h5>"
    )
    tool_difficult_steps4 = models.BooleanField(
        label="<h5> Is the processing step <b>resolve multiple headers</b> necessary to prepare the data for analysis </h5>"
    )
    tool_difficult_steps5 = models.BooleanField(
        label=" <h5> Is the processing step <b>split cells containing multiple values into new columns</b> necessary to prepare the data for analysis </h5>"
    )

    tool_difficult_col1 = models.StringField(
        label="<h5> Based on the data, which column names are most suitable for the transformed data? </h5>",
        choices=[["area", "Area, Main means of transport, Delay due to, Time of day"],
            ["location", "Location, Vehicle, Time of day, Minutes"],
            ["city", "City, Means of transport, Cause, Time, Duration"],
           ["accident", "Accident location, Participant, Cause, Rescue time"]
        ],
        widget=widgets.RadioSelect
    )

#Treatment B
#easy
    excel_easy_problem1 = models.StringField(
            label="<h5> How would you restructure this data so that it can be stored in a relational database? </h5>",
            choices=[
            ["A", "District, Gender, Age from, Age to, Amount "],
            ["B", "Gender, Age and District organized in Rows, Amounts assigned to columns"],
            ["C", "District, Gender, Age, Amount "],
            ["D", "Simple listing of values without specific column labels"],
            ],
            widget=widgets.RadioSelect
    )

    excel_easy_problem2 = models.StringField(
            label="<h5> What is a common problem in the given dataset? </h5>",
            choices=[
            ["headers", "Missing column headers"],
            ["delimiters", "Inconsistent use of delimiters"],
            ["assignment", "Assignment of values to multiple attributes"],
            ["keys", "Duplicate primary keys"],
            ],
            widget=widgets.RadioSelect
    )

    excel_easy_problem3 = models.StringField(
            label="<h5> Which characteristic shows that the dataset is in a wide rather than a tidy structure? </h5>",
            choices=[
            ["exactly_three", "A tidy table must always have exactly three columns: “Variable”, “Value”, and “ID”. This is not the case in this dataset"],
            ["missing_values", "The dataset is not a tidy table because wide tables always contain more missing values than tidy tables."],
            ["gender_age", "The dataset is not in a tidy structure because the attributes Gender and Age are spread across multiple columns."],
            ["repeated_values", "The dataset is a tidy table which can be recognized by the fact that values are repeated across different cells."],
            ["unique_names", "The dataset is a wide table because there are unique column names."],
            ],
            widget=widgets.RadioSelect
    )

    excel_easy_problem4 = models.StringField(
            label="<h5> How could you edit the wide table to get a tidy table? </h5>",
            choices=[
            ["clear_names", "I should label the columns more clearly to show the assignment of values more clearly. It is not necessary to restructure the table for this."],
            ["pivot", "I should pivot the table to transfer the values of a variable into a column."],
            ["delete", "I delete duplicate data."],
            ["new", "I create new tables to store the attributes uniquely."],
            ["detailed", "I am adding additional columns to record the attributes in more detail."],
            ],
            widget=widgets.RadioSelect
    )

#difficult
    excel_difficult_problem1 = models.StringField(
        label="<h5> What problem areas do you identify in the raw data and how would you deal with these challenges in each case? </h5>",
        choices=[
           ["invalid characters" , "Invalid characters: Replace special characters with appropriate values."],
           ["inconsistent spellings", "Inconsistent spellings in text categories: Standardize them using mapping or text normalization (lowercasing, removing special characters)."],
           ["missing values", "Missing values: Decide whether to fill in missing entries through imputation or remove rows with too many missing values."]
        ],
        widget=widgets.RadioSelect
    )

    excel_difficult_problem2 = models.StringField(
        label="<h5> What further problem areas do you identify? </h5>",
        choices=[["duplicates","Duplicates: Identify and remove duplicate entries to ensure data quality."],
            ["no problems", "Data is already completely clean and requires no further processing."],
           ["missing col names", "Missing column names: add to each column a unique name",]
        ],
        widget=widgets.RadioSelect
    )

    excel_difficult_steps1 = models.BooleanField(
        label="<h5> Did you <b> replace individual values with new values </b> in the raw data? </h5>"
    )

    excel_difficult_steps2 = models.BooleanField(
        label="<h5> Did you <b> change column names </b> in the raw data?  </h5>"
    )

    excel_difficult_steps3 = models.BooleanField(
        label="<h5> Did you <b> delete duplicate entries </b> in the raw data?  </h5>"
    )

    excel_difficult_steps4 = models.BooleanField(
        label="<h5> Did you <b> split values from one column into several new columns </b> in the raw data? </h5>"
    )

    excel_difficult_steps5 = models.BooleanField(
        label="<h5> Did you <b> convert time units </b> in the raw data? </h5>"
    )

    excel_difficult_col1 = models.StringField(
        label="<h5> Based on the data, which column names are most suitable for the transformed data? </h5>",
        choices=[["area", "Area, Main means of transport, Delay due to, Time of day"],
            ["location", "Location, Vehicle, Time of day, Minutes"],
            ["city", "City, Means of transport, Cause, Duration"],
           ["accident", "Accident location, Participant, Cause, Rescue time"]
        ],
        widget=widgets.RadioSelect
    )

    # Post-questionnaire
    post_experience = models.LongStringField(
        label="Please describe your experience using the tool.",
        blank=True
    )
    difficulties = models.LongStringField(
        label="What difficulties did you encounter, if any?",
        blank=True
    )
    satisfaction = models.StringField(
        label="How satisfied are you with the tool?",
        choices=["very satisfied", "satisfied",  "neutral", "dissatisfied", "very dissatisfied"],
        widget=widgets.RadioSelectHorizontal
    )

    # File tracking
    #uploaded_filename = models.StringField(blank=True)
