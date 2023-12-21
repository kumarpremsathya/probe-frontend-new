from django import forms


class DateRangeFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.TextInput(attrs={'type': 'date'}))


# class DateRangeFilterForm(forms.Form):
#     start_date = forms.DateField(label='Start Date', required=False, widget=forms.TextInput(attrs={'type': 'date'}))
#     end_date = forms.DateField(label='End Date', required=False, widget=forms.TextInput(attrs={'type': 'date'}))