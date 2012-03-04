from django.forms import ModelForm, CharField
from django.contrib.auth.models import User


class UserForm(ModelForm):
    # todo: mask password
    password = CharField()
    
    class Meta:
        model = User
        # todo: make email required
        fields = ['username', 'email']

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        user = super(UserForm, self).save(*args, **kwargs)

        user.set_password(self.cleaned_data['password'])
        user.save()

        return user


