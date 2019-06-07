class Page(list):

    def __init__(self, collection, pager=1, page=1, items_per_page=20, item_count=None, wrapper_class=None):
        self.pager = pager

        if collection is not None:
            if wrapper_class is None:
                # Default case. The collection is already a list-type object.
                self.collection = collection
            else:
                # Special case. A custom wrapper class is used to access elements of the collection.
                self.collection = wrapper_class(collection)
        else:
            self.collection = []

        if self.pager:
            self.collection_type = type(collection)

            try:
                self.page = int(page)  # make it int() if we get it as a string
            except (ValueError, TypeError):
                self.page = 1

            self.items_per_page = items_per_page

            if item_count is not None:
                self.item_count = item_count
            else:
                try:
                    self.item_count = len(self.collection)
                except Exception as e:
                    self.item_count = len(self.collection)

            # Compute the number of the first and last available page
            if self.item_count > 0:
                self.first_page = 1
                self.page_count = ((self.item_count - 1) // self.items_per_page) + 1
                self.last_page = self.first_page + self.page_count - 1

                # Make sure that the requested page number is the range of valid pages
                if self.page > self.last_page:
                    self.page = self.last_page
                elif self.page < self.first_page:
                    self.page = self.first_page

                # Note: the number of items on this page can be less than
                #       items_per_page if the last page is not full
                self.first_item = (self.page - 1) * items_per_page + 1
                self.last_item = min(self.first_item + items_per_page - 1, self.item_count)

                # We subclassed "list" so we need to call its init() method
                # and fill the new list with the items to be displayed on the page.
                # We use list() so that the items on the current page are retrieved
                # only once. In an SQL context that could otherwise lead to running the same
                # SQL query every time items would be accessed.
                try:
                    first = self.first_item - 1
                    last = self.last_item
                    self._items = list(self.collection[first:last])
                except TypeError:
                    raise TypeError(f"Your collection of type {type(self.collection)} cannot be handled by paginate.")

                # Links to previous and next page
                if self.page > self.first_page:
                    self.previous_page = self.page - 1
                else:
                    self.previous_page = None

                if self.page < self.last_page:
                    self.next_page = self.page + 1
                else:
                    self.next_page = None

            # No items available
            else:
                self.first_page = None
                self.page_count = 0
                self.last_page = None
                self.first_item = None
                self.last_item = None
                self.previous_page = None
                self.next_page = None
                self._items = []
        else:
            self._items = self.collection
        # This is a subclass of the 'list' type. Initialise the list now.
        list.__init__(self, self.items)

    def __str__(self):
        return ("Page:\n"
                "Collection type:        {0.collection_type}\n"
                "Current page:           {0.page}\n"
                "First item:             {0.first_item}\n"
                "Last item:              {0.last_item}\n"
                "First page:             {0.first_page}\n"
                "Last page:              {0.last_page}\n"
                "Previous page:          {0.previous_page}\n"
                "Next page:              {0.next_page}\n"
                "Items per page:         {0.items_per_page}\n"
                "Total number of items:  {0.item_count}\n"
                "Number of pages:        {0.page_count}\n"
                ).format(self)

    def __repr__(self):
        return ("<paginate.Page: Page {0}/{1}>".format(self.page, self.page_count))

    @property
    def info(self):
        if self.pager:
            return {
                "item_count": self.item_count,
                "first_page": self.first_page,
                "page_count": self.page_count,
                "last_page": self.last_page,
                "first_item": self.first_item,
                "last_item": self.last_item,
                "previous_page": self.previous_page,
                "next_page": self.next_page,
                "item_per_page": self.items_per_page
            }
        else:
            return {}

    @property
    def items(self):
        return self._items
