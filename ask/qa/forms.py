from django import forms

from qa.models import Question, Answer, User

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)
    _user = None

    def clean(self):
        return self.cleaned_data
    
    def save(self, id):
        answer = Answer(question_id=id, 
                text=self.cleaned_data['text'],
                author=self._user)
        answer.save()
        return answer


class AskForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    _user = None 

    def clean(self):
        return self.cleaned_data

    def save(self):
        question = Question(title=self.cleaned_data['title'], 
                text=self.cleaned_data['text'],
                author=self._user)
        question.save()
        return question   

