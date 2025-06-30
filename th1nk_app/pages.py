from otree.api import *
import os
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect

from .models import C, Subsession, Group, Player

class PreQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['prior_knowledge', 'motivation']


class ToolAndUpload(Page):
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


class PostQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['post_experience', 'difficulties', 'satisfaction']

page_sequence = [PreQuestionnaire, ToolAndUpload, PostQuestionnaire]
