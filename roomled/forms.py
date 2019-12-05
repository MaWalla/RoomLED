from django import forms
from django.core.exceptions import ValidationError


class MainForm(forms.Form):

    def clean(self):
        cleaned_data = {}
        for key, value in self.data.items():
            if key[:7] == 'nodemcu':
                if value == 'on':
                    cleaned_data[key] = True
            elif key[:5] == 'color':
                if len(value) == 7 and value[0] == '#':
                    cleaned_data[key] = self.color_convert(value)
                else:
                    return ValidationError('Invalid color code, must be like #123ABC')
            else:
                cleaned_data[key] = value

        return cleaned_data

    @staticmethod
    def color_convert(color):
        color = color.lstrip('#')
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
