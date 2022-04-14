from django.http.response import Http404
from django.views.generic.list import ListView
from django.core.paginator import InvalidPage, Paginator
from django.utils.translation import gettext_lazy as _

class PaginatedListView(ListView):
    """
    Mixin class adding pagination feature for ListView.
    이동건/2021.10.28
    """
    
    paginate_window_half = 4
    handle_404 = True
    current_page = None

    # Override
    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)

            # Handle page overflow.
            if self.handle_404:
                if page_number > paginator.num_pages:
                    page_number = paginator.num_pages
                elif page_number < 1:
                    page_number = 1

            self.current_page = page_number
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        # Calculate pagination window.
        paginator: Paginator = context.get('paginator', None)
        if paginator:
            current_page = self.current_page - 1

            left_bound = current_page - self.paginate_window_half
            right_bound = current_page + self.paginate_window_half
            if left_bound < 0:
                right_bound += abs(left_bound)
                left_bound = 0
            exceed_page = right_bound - len(paginator.page_range) + 1
            if exceed_page > 0:
                right_bound = len(paginator.page_range)
                left_bound = 0 if left_bound - exceed_page < 0 else left_bound - exceed_page

            page_range = paginator.page_range[left_bound:right_bound+1]

            context['page_range'] = page_range
            context[self.page_kwarg] = current_page + 1
        else:
            context['is_paginated'] = False

        return context