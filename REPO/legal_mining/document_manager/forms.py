from django import forms
from haystack.forms import SearchForm


WHERE_OPTIONS = [('both', 'In Text and Title'), ('title', 'In Title only'), ('text', 'In Text only')]
LANGUAGE_OPTIONS = [('all', 'All'), ('german', 'German only'), ('english', 'English only'), ('french', 'French only'), ('spanish', 'Spanish only')]
SOURCE_OPTIONS = [('all', 'All'), ('eur_parl', 'European Parliament'), ('oecd', 'OECD'), ('bundesministerium', 'Bundesministerium der Finanzen')]

class CustomSearchForm(SearchForm):

    # overriding q
    q = forms.CharField(required=False, label='Search',
                        widget=forms.TextInput(attrs={'type': 'search', 'class': 'form-control', 'id':'q'}))

    where_to_search = forms.ChoiceField(widget=forms.Select(attrs={'id':'where', 'class': 'form-control'}), label='Search in:', choices=WHERE_OPTIONS, required=True)
    language = forms.ChoiceField(widget=forms.Select(attrs={'id':'language', 'class': 'form-control'}), label='Language:', choices=LANGUAGE_OPTIONS, required=False)
    source = forms.ChoiceField(widget=forms.Select(attrs={'id':'source', 'class': 'form-control'}), label='Source:', choices=SOURCE_OPTIONS, required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(CustomSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # filtering only if not both is chosen
        if not self.cleaned_data['where_to_search'] == 'both':
            if self.cleaned_data['where_to_search'] == 'title':
                sqs = sqs.filter(text=self.cleaned_data['q'])
            if self.cleaned_data['where_to_search'] == 'text':
                sqs = sqs.filter(text2=self.cleaned_data['q'])

        if not self.cleaned_data['language'] == 'all':
            if self.cleaned_data['language'] == 'german':
                sqs = sqs.filter(language=1)
            if self.cleaned_data['language'] == 'english':
                sqs = sqs.filter(language=2)
            if self.cleaned_data['language'] == 'french':
                sqs = sqs.filter(language=3)
            if self.cleaned_data['language'] == 'spanish':
                sqs = sqs.filter(language=4)

        if not self.cleaned_data['source'] == 'all':
            if self.cleaned_data['source'] == 'bundesministerium':
                sqs = sqs.filter(datasource=1)
            if self.cleaned_data['source'] == 'oecd':
                sqs = sqs.filter(datasource=2)
            if self.cleaned_data['source'] == 'eur_parl':
                sqs = sqs.filter(datasource=3)

        return sqs
