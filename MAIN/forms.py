from django.forms import ModelForm
from .models import Project, Message




class Avtomat_input:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "input input--text",
                }
            )

class ProjectForm(Avtomat_input,ModelForm):
    class Meta:
        model = Project
        fields = ["name", "discription", "image", "source_link", "demo_link"]



class MessageForm(Avtomat_input,ModelForm):
    class Meta:
        model = Message
        fields = ["fullname", "email", "subject", "body"]
