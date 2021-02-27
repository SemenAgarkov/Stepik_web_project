from django import forms

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def clean_text(self):
        text = self.cleaned_data['text']
        if not is_ethic(text):
            raise forms.ValidationError(u'Сообщение не корректно', code=12)
        return text + \
            "\nThank you for your attention."

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question



class AnswerForm(forms.Form):
    text = forms.Textarea(default="")
    question = forms.CharField(widget=forms.Textarea)

    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            question = None
        return question
        if not is_ethic(question):
            raise forms.ValidationError(u'Сообщение не корректно', code=12)
        return question + \
               "\nThank you for your attention."

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = self._user.id
        answer.save()
        return answer


