from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UserModel


class userModelCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserModel
        fields = ('Username',)


class userModelChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('Username',)
