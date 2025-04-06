from typing import List, Dict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10

class CustomPagination(PageNumberPagination):

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data: List[Dict], additional_info: Dict = None) -> Response:

        response_data = {
            'previous_page': self.get_previous_link(),
            'next_page':self.get_next_link(),
            'current_page': self.page.number,
            'total_items': self.page.paginator.count,
            'data':data
        }

        if additional_info:
            response_data["additional_information"] = additional_info

        return Response(data=response_data)

