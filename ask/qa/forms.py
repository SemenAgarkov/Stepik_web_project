from django import forms

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
'''
    def __init__(self, user, **kwargs):
        self._user = user
        super(AddPostForm, self).__init__(**kwargs)

    def clean(self):
        if self._user.is_banned:
            raise ValidationError(u'Access denied')

    def save(self):
        self.cleaned_data['author'] = self._user
        return Post.objects.create(**self.cleaned_data)
'''

    def clean_text(self):
        pass

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.Textarea(default="")
    question = forms.CharField(widget=forms.Textarea)
'''
    def __init__(self, user, **kwargs):
        self._user = user
        super(AddPostForm, self).__init__(**kwargs)


    def clean(self):
        if self._user.is_banned:
            raise ValidationError(u'Access denied')


    def save(self):
        self.cleaned_data['author'] = self._user
        return Post.objects.create(**self.cleaned_data)
'''
    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            question = None
        return question

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = self._user.id
        answer.save()
        return answer


