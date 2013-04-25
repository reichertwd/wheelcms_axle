from django import forms
from django.core.urlresolvers import reverse


from two.ol.base import FormHandler
from wheelcms_axle.models import Configuration
from wheelcms_axle.base import WheelHandlerMixin

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration

    theme = forms.ChoiceField(choices=(
        ('default', 'Bootstrap'),
        ('amelia', 'Amelia'),
        ('cerulean', 'Cerulean'),
        ('cosmo', 'Cosmo'),
        ('cyborg', 'Cyborg'),
        ('journal', 'Journal'),
        ('readable', 'Readable'),
        ('simplex', 'Simplex'),
        ('slate', 'Slate'),
        ('spruce', 'Spruce'),
        ('superhero', 'Superhero'),
        ('united', 'United')))

class ConfigurationHandler(FormHandler, WheelHandlerMixin):
    def index(self):
        if not self.hasaccess():
            return self.forbidden()

        instance = Configuration.config()
        self.context['form'] = ConfigurationForm(instance=instance)
        ## set redirect_to
        return self.template("wheelcms_axle/configuration.html")

    def process(self):
        instance = Configuration.config()
        self.context['form'] = form = \
                 ConfigurationForm(self.request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return self.redirect(reverse('wheel_config'), success="Changes saved")
        return self.template("wheelcms_axle/configuration.html")
