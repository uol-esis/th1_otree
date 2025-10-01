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

    LIKERT_CHOICES = [
        (7, "Strongly disagree"),
        (6, "Disagree"),
        (5, "Rather disagree"),
        (4, "Neutral"),
        (3, "Rather agree"),
        (2, "Agree"),
        (1, "Strongly agree"),
    ]

LIKERT_CHOICES = [
    (7, "Strongly disagree"),
    (6, "Disagree"),
    (5, "Rather disagree"),
    (4, "Neutral"),
    (3, "Rather agree"),
    (2, "Agree"),
    (1, "Strongly agree"),
]



class Subsession(BaseSubsession):
    def creating_session(self):
        #A = Tool, B = Excel
        for p in self.get_players():
            #p.treatment = random.choice(C.TREATMENT)
            p.treatment = 'A'

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    treatment = models.StringField()
    score = models.IntegerField(initial=0)
    attention_failed = models.BooleanField(initial=False)

    # Introduction
    prolificID = models.StringField(label='Please enter your Prolific ID:')
    age = models.IntegerField(label='How old are you?')
    gender = models.StringField(
        choices=['male', 'female', 'diverse'],
        label='What is your gender?'
    )
    employment_status = models.StringField(
        choices=['Full-time employed',
        'Part-time employed',
        'Self-employed',
        'Unemployed',
        'Student',
        'Intern/Apprentice',
        'Other'],
        label='What is your employment status?'
    )
    job_type = models.StringField(
        choices=['Information Technology / Data',
        'Education / Academia',
        'Healthcare',
        'Business / Management',
        'Engineering / Technical',
        'Other'],
        label='What is your job type?'
    )
    education = models.StringField(
        choices=['Apprenticeship','Diploma below college level', 'Bachelor\'s degree', 'Master\'s degree', 'Ph.D. or higher degree'],
        label='What is the highest level of education that you have completed?'
    )

    # Pre-questionnaire
    # --- Data Identification (DI) ---
    DLSE_DI1 = models.IntegerField(label="I can define what data is.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DI2 = models.IntegerField(label="I am able to describe different types of data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DI3 = models.IntegerField(label="I am aware of various formats in which data can be stored.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DI4 = models.IntegerField(label="I am able to find data that is relevant to me.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DI5 = models.IntegerField(label="I am able to explain data from my area of responsibility.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DI6 = models.IntegerField(label="I know how to collect data that is relevant to me.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DI7 = models.IntegerField(label="I know how to access the data relevant to me.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)

    # --- Data Processing (DP) ---
    DLSE_DP1 = models.IntegerField(label="I am able to assess the quality of data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP2 = models.IntegerField(label="I am able to create summarized reports on the data available to me.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP3 = models.IntegerField(label="I know how to create diagrams based on data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP4 = models.IntegerField(label="I know how to create summary tables from data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP5 = models.IntegerField(label="I am able to interpret data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP6 = models.IntegerField(label="I am able to derive predictions from data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP7 = models.IntegerField(label="I am able to find patterns in data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP8 = models.IntegerField(label="I am able to create reports based on data analysis.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP9 = models.IntegerField(label="I am able to communicate the results of data analyses.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP10 = models.IntegerField(label="I know which tools I need to use for data visualizations.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP11 = models.IntegerField(label="I am able to explain data visualizations.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP12 = models.IntegerField(label="I am able to develop a narrative from a data analysis.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP13 = models.IntegerField(label="I am able to assess whether a data source is relevant for me.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP14 = models.IntegerField(label="I am able to categorize data according to its content.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP15 = models.IntegerField(label="I am able to organize data on my computer.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DP16 = models.IntegerField(label="I am able to determine a convention for versioning data records.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)

    # --- Data Sharing & Management (DMS) ---
    DLSE_DMS1 = models.IntegerField(label="I know how to document data for others.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DMS2 = models.IntegerField(label="I am able to make data accessible to others.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DMS3 = models.IntegerField(label="I can distinguish whether data is stored on my computer or in the cloud.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DMS4 = models.IntegerField(label="I know how to save data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DMS5 = models.IntegerField(label="I know methods for storing data that are worth protecting under data protection law.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DMS6 = models.IntegerField(label="I know the laws and regulations on the protection of personal data.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DMS7 = models.IntegerField(label="I know who has which data in my organization.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)
    DLSE_DMS8 = models.IntegerField(label="I know which data I am allowed to use.", choices=LIKERT_CHOICES, widget=widgets.RadioSelectHorizontal)

#Attention checks
    data_attention_1 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=[["first", "I understand the practices used to share the significance of data."], 
                 ["second", "I understand the effects of using good practices to communicate the meaning of data."], 
                 ["third", "I'm capable of understanding the background of data."], 
                 ["fourth", "My current work requires me to implement this skill."], 
                 ["fifth", "My current level in this skill is sufficient to carry out my work."]
                 ],
        widget=widgets.RadioSelect
    )

    data_attention_3 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=[["first", "I understand the practices used to share the significance of data."], 
                 ["second", "I understand the effects of using good practices to communicate the meaning of data."], 
                 ["third", "I'm capable of understanding the background of data."], 
                 ["fourth", "My current work requires me to implement this skill."], 
                 ["fifth", "My current level in this skill is sufficient to carry out my work."]
                 ],
        widget=widgets.RadioSelect
    )

    data_attention_4 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=[["first", "I understand the practices used to share the significance of data."], 
                 ["second", "I understand the effects of using good practices to communicate the meaning of data."], 
                 ["third", "I'm capable of understanding the background of data."], 
                 ["fourth", "My current work requires me to implement this skill."], 
                 ["fifth", "My current level in this skill is sufficient to carry out my work."]
                 ],
        widget=widgets.RadioSelect
    )

    data_attention_5 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=[["first", "I understand the practices used to share the significance of data."], 
                 ["second", "I understand the effects of using good practices to communicate the meaning of data."], 
                 ["third", "I'm capable of understanding the background of data."], 
                 ["fourth", "My current work requires me to implement this skill."], 
                 ["fifth", "My current level in this skill is sufficient to carry out my work."]
                 ],
        widget=widgets.RadioSelect
    )

    data_attention_6 = models.StringField(
        label="<h5> To show you are paying attention, please select the third answer for this question. </h5>",
        choices=[["first", "I understand the practices used to share the significance of data."], 
                 ["second", "I understand the effects of using good practices to communicate the meaning of data."], 
                 ["third", "I'm capable of understanding the background of data."], 
                 ["fourth", "My current work requires me to implement this skill."], 
                 ["fifth", "My current level in this skill is sufficient to carry out my work."]
                 ],
        widget=widgets.RadioSelect
    )

    data_attention_2 = models.IntegerField(
            label="I am able to click “Strongly agree”.",
            choices= LIKERT_CHOICES,
            widget=widgets.RadioSelectHorizontal
    )

    data_attention_7 = models.StringField(
            label="<h5> Which of the following is a common way to organize data? </h5>",
            choices=[
                ["papers","By throwing papers randomly on the floor"], 
                ["rows" ,"In rows and columns"], 
                ["memory", "By using only your memory without writing anything down"], 
                ["doodles","In drawn doodles on a napkin"], 
                ["numbers","By singing the numbers out loud instead of writing them down"]
            ],
            widget=widgets.RadioSelect
    )
#Manipulation check
    manipulation_check_A = models.StringField(
            label="<h5> What is your main task in this part of the study? </h5>",
            choices=["To transform the dataset into a presentation with charts and figures.",
                        "To restructure the dataset using the provided tool to get a tidy table.",
                        "To reduce the dataset so that only a small sample remains.",
                        "To freely modify the dataset according to your own preferences, without following specific rules."],
            widget=widgets.RadioSelect
    )

    manipulation_check_B = models.StringField(
            label="<h5> What is your main task in this part of the study? </h5>",
            choices=["To transform the dataset into a presentation with charts and figures.",
                        "To restructure the dataset using Excel, for example, to get a tidy table.",
                        "To reduce the dataset so that only a small sample remains.",
                        "To freely modify the dataset according to your own preferences, without following specific rules."],
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
        ['false format', 'The values are not properly formatted to analyze them.'],
        ['multiple attributes' , 'The values depend on variables, each spans multiple columns.'],
        ['not normalized', 'The nested structure of the variables is too simple, so it can only be cleaned up by deleting columns.'],
        ['flat structure','The structure is flat and clean, but the cells content too much information which cannot be processed accurately']
        ],
        label='<h5> Why is the nested structure of the dataset problematic? </h5>',
        widget=widgets.RadioSelect
    )

    tool_easy_problem2 = models.StringField(choices= [
       ['complex structure' ,'The structure got more complex.'],
        ['duplicates', 'Many duplicates were created.'],
        ['changed format', 'The data format has changed.'],
        ['one col attributes', 'Each attribute now consists of only one column.']
        ],
        label='<h5> What has changed in the transformation process? </h5>',
        widget=widgets.RadioSelect
    )

#difficult
    tool_difficult_problem1 = models.StringField(
        label="<h5> What problem areas do you identify in the raw data and how would you deal with these challenges in each case? </h5>",
        choices=[
           ["invalid characters" , "Invalid values: Correct them with appropriate values if possible or remove them."],
           ["inconsistent spellings", "Inconsistent spellings in text categories: Standardize them using mapping or text normalization (e.g. lowercasing)."],
           ["missing values", "Missing cell entries: Decide whether to fill in missing entries through assumptions or remove rows with too many missing values."]
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
        label="<h5> Is the processing step <b>remove duplicates</b> necessary for this dataset to achieve a tidy format?</h5>"
    )

    tool_difficult_steps2 = models.BooleanField(
        label="<h5>  Is the processing step <b>remove rows with invalid values</b> necessary for this dataset to achieve a tidy format?</h5>"
    )
    tool_difficult_steps3 = models.BooleanField(
        label="<h5> Is the processing step <b>add column headers</b> necessary for this dataset to achieve a tidy format?</h5>"
    )
    tool_difficult_steps4 = models.BooleanField(
        label="<h5> Is the processing step <b>resolve multiple headers</b> necessary for this dataset to achieve a tidy format?</h5>"
    )
    tool_difficult_steps5 = models.BooleanField(
        label=" <h5> Is the processing step <b>split cells containing multiple values into new columns</b> necessary for this dataset to achieve a tidy format?</h5>"
    )

    tool_difficult_col1 = models.StringField(
        label="<h5> Based on the data, which column names are most suitable for the transformed data? </h5>",
        choices=[["city", "City,  Means of transport, Reason for delay, Minutes"],
            ["location", "Location, Vehicle, Destination, Duration"],
            ["area", "Area, Means of transport, Cause, Time, Duration"],
           ["accident", "Accident location, Participant, Cause, Rescue time"]
        ],
        widget=widgets.RadioSelect
    )

#Treatment B
#easy
    excel_easy_problem1 = models.StringField(
            label="<h5> How would you restructure this data so that it complies with the requirements for a tidy format? </h5>",
            choices=[
            ["A", "District, Gender, Age from, Age to, Amount "],
            ["B", "Gender, Age and District organized in Rows, Amounts assigned to columns"],
            ["C", "District, Gender, Age, Amount "],
            ["D", "Simple listing of values without specific column labels"],
            ],
            widget=widgets.RadioSelect
    )

    excel_easy_problem2 = models.StringField(
            label="<h5> What is the main problem in the given dataset? </h5>",
            choices=[
            ["headers", "Missing column headers"],
            ["delimiters", "Inconsistent use of delimiters"],
            ["assignment", "Assignment of values to multiple variables"],
            ["keys", "Duplicate primary keys"],
            ],
            widget=widgets.RadioSelect
    )

    excel_easy_problem4 = models.StringField(
        label="<h5> How could you edit the data to get a tidy table? </h5>",
        choices=[
        ["clear_names", "I should label the columns more clearly. It is not necessary to restructure the table for this."],
        ["pivot", "I should reorder parts of the table to transfer the values of a variable into one column."],
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
           ["invalid characters" , "Invalid values: Replace special characters with appropriate values."],
           ["inconsistent spellings", "Inconsistent spellings in text categories: Standardize them using mapping or text normalization (lowercasing, removing special characters)."],
           ["missing values", "Missing cell entries: Decide whether to fill in missing entries through imputation or remove rows with too many missing values."]
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
        label="<h5> Is the processing step <b>remove duplicates</b> necessary for this dataset to achieve a tidy format?</h5>"
    )

    excel_difficult_steps2 = models.BooleanField(
        label="<h5>  Is the processing step <b>remove rows with invalid values</b> necessary for this dataset to achieve a tidy format?</h5>"
    )

    excel_difficult_steps3 = models.BooleanField(
        label="<h5> Is the processing step <b>add column headers</b> necessary for this dataset to achieve a tidy format?</h5>"
    )

    excel_difficult_steps4 = models.BooleanField(
       label="<h5> Is the processing step <b>resolve multiple headers</b> necessary for this dataset to achieve a tidy format?</h5>"
    )

    excel_difficult_steps5 = models.BooleanField(
        label=" <h5> Is the processing step <b>split cells containing multiple values into new columns</b> necessary for this dataset to achieve a tidy format?</h5>"
    )

    excel_difficult_col1 = models.StringField(
        label="<h5> Based on the data, which column names are most suitable for the transformed data? </h5>",
        choices=[["city", "City,  Means of transport, Reason for delay, Minutes"],
            ["location", "Location, Vehicle, Destination, Duration"],
            ["area", "Area, Means of transport, Cause, Time, Duration"],
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
        label="What difficulties did you encounter during this study, if any?",
        blank=True
    )
    satisfaction = models.StringField(
        label="How satisfied are you with the tool?",
        choices=["very satisfied", "satisfied",  "neutral", "dissatisfied", "very dissatisfied"],
        widget=widgets.RadioSelectHorizontal
    )

    # File tracking
    #uploaded_filename = models.StringField(blank=True)
