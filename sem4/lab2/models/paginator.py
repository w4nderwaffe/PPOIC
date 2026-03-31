import math


class Paginator:
    def __init__(self, items, page_size: int = 10, current_page: int = 1):
        self.items = list(items)
        self.page_size = max(1, int(page_size))
        self.current_page = max(1, int(current_page))

    @property
    def total_items(self) -> int:
        return len(self.items)

    @property
    def total_pages(self) -> int:
        if self.total_items == 0:
            return 1
        return math.ceil(self.total_items / self.page_size)

    def get_page_items(self):
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages

        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.items[start:end]

    def first_page(self):
        self.current_page = 1

    def last_page(self):
        self.current_page = self.total_pages

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def set_page_size(self, page_size: int):
        self.page_size = max(1, int(page_size))
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages

    def set_page(self, page: int):
        page = int(page)
        if page < 1:
            self.current_page = 1
        elif page > self.total_pages:
            self.current_page = self.total_pages
        else:
            self.current_page = page