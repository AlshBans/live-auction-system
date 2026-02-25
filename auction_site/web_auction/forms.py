from django import forms
from .models import Auction

class AuctionForm(forms.ModelForm):
    priority = forms.IntegerField(
        label='Priority',
        min_value=1,
        max_value=10,
        initial=5,
        help_text='Enter priority for auction item'
    )

    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        label='Start Time',
        help_text='Select the start date and time for the auction'
    )

    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        label='End Time',
        help_text='Select the end date and time for the auction'
    )

    class Meta:
        model = Auction
        fields = ['title', 'description', 'base_amount', 'start_time', 'end_time', 'priority','image']

