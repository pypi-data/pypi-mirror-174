from rest_framework import pagination

from rest_framework.utils.urls import replace_query_param


class ErpPagination(pagination.PageNumberPagination):
    '''
    List request without parameters defaults to showing all objects up to max_page_size
    '''
    max_page_size = 10000000
    page_size_query_param = 'page_size'  # items per page

    def get_page_size(self, request):
        if 'page' not in request.query_params:
            return self.max_page_size
        return super(ErpPagination, self).get_page_size(request)

    def get_previous_link(self):
        """
        Overides default removal of page=1 parameter for previous link
        :return:
        """
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_html_context(self):
        """
        Overides default removal of page=1 parameter for previous link
        :return: dict
        """
        base_url = self.request.build_absolute_uri()

        def page_number_to_url(page_number):
            return replace_query_param(base_url, self.page_query_param, page_number)

        current = self.page.number
        final = self.page.paginator.num_pages
        page_numbers = pagination._get_displayed_page_numbers(current, final)
        page_links = pagination._get_page_links(page_numbers, current, page_number_to_url)

        return {
            'previous_url': self.get_previous_link(),
            'next_url': self.get_next_link(),
            'page_links': page_links
        }
