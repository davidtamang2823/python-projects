from typing import List, Dict
from rest_framework.pagination import BasePagination
from rest_framework.response import Response

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PER_PAGE = 10

class CustomPagination(BasePagination):

    def get_paginated_response(self, data: List[Dict], additional_info: Dict = None) -> Response:

        response_data = {
            'previous_page': '',
            'next_page':'',
            'page_size': '',
            'total_item':'',
            'data':data
        }

        if additional_info:
            response_data["additional_information"] = additional_info

        return Response(data=response_data)

