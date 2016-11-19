from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm

class ModelBase(object):
	query_class = BaseQuery
	query = None

	Model = declarative_base(cls=ModelBase)

class BaseQuery(orm.Query):

	def paginate(self, page,per_page = 20, error_out = True):

		if error_out and page <1:
			raise IndexError


		if per_page is None:
			per_page = self.DEFAULT_PER_PAGE

		items = self.page(page,per_page).all()

		if not items and page != 1 and error_out:
			raise IndexError

		if page == 1 and len(items) < per_page:
			total = len(items)
		else:
			total = self.order_by(None).count()

		return Pagination (self, page,per_page,total,items)

class Pagination(object):
	
	def __init__(self, query, page, per_page, total, items):
		self.query = query
		self.page = page
		self.per_page = per_page
		self.total = total
		self.items = items

		if self.per_page == 0:
			self.pages = 0
		else:
			self.pages = int(ceil(self.total / float(self.per_page)))
		self.prev_num = self.page - 1
		self.has_prev = self.page > 1
		self.next_num = self.page + 1.
		self.has_next = self.page < self.pages

	def prev(self, error_out=False):
		assert self.query is not None, \
			'a query object is required for this method to work'
		return self.query.paginate(self.page - 1, self.per_page, error_out)

	def next(self, error_out=False):
		assert self.query is not None, \
			'a query object is required for this method to work'
		return self.query.paginate(self.page + 1, self.per_page, error_out)


class QueryProperty(object):

    def __init__(self, session):
        self.session = session

    def __get__(self, model, Model):
        mapper = orm.class_mapper(Model)

        if mapper:
            if not getattr(Model, 'query_class', None):
                Model.query_class = BaseQuery

            query_property = Model.query_class(mapper, session=self.session())

            return query_property
    def set_query_property(model_class, session):
    	model_class.query = QueryProperty(session)