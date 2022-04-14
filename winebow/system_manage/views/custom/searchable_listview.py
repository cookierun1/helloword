from typing import Any, Dict, List
from django.db.models.query import QuerySet
from django.views.generic import ListView

class CriteriaNamePair:
    def __init__(self, name, showing_name):
        self.name = name
        self.showing_name = showing_name

class SearchableListView(ListView):
    """
    Mixin class adding searching feature for ListView.
    이동건/2021.10.28
    """

    criteria_key = "criteria"
    search_keyword_key = "search_keyword"

    IF_CRITERIA: List[CriteriaNamePair]= [
        # List of key and showing name pair.
    ]

    SEARCH_CRITERIA: Dict[str, str] = { 
        # List of key and database column name.
    }

    def get_queryset(self) -> QuerySet:
        criteria = self.request.GET.get(self.criteria_key, None)
        keyword = self.request.GET.get(self.search_keyword_key, "")

        # Filter search criteria.
        if criteria in self.SEARCH_CRITERIA.keys():
            return self.search_queryset(keyword, self.SEARCH_CRITERIA[criteria])
        else:
            return super().get_queryset()
        
    def search_queryset(self, keyword, db_column) -> QuerySet:
        raise NotImplemented

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['criteria_list'] = self.IF_CRITERIA
        context['criteria'] = self.request.GET.get('criteria', '')
        context['search_keyword'] = self.request.GET.get('search_keyword', '')

        return context