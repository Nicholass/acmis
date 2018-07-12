# -*- coding: utf-8
from __future__ import unicode_literals

from wiki.editors.base import BaseEditor
from simplemde.widgets import SimpleMDEEditor

class SimpleMDE(BaseEditor):
    editor_id = 'markitup'

    def get_admin_widget(self, instance=None):
        return SimpleMDEEditor()

    def get_widget(self, instance=None):
        return SimpleMDEEditor()