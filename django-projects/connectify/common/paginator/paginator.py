from typing import List, Dict
from django.core.paginator import Paginator

class PaginatorCommon:


    def get_paginator_response(self, data: List[Dict], page_size: int, page: int) -> Dict:
        paginator_object = Paginator(object_list=data, per_page=page_size)
        page_obj = paginator_object.get_page(page)

        paginated_details = {
            "current_page_number": page_obj.number,
            "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "total_pages": page_obj.paginator.num_pages,
            "total_items": page_obj.paginator.count,
            "data": page_obj.object_list,
        }

        return paginated_details