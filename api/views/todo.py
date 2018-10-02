# -*- coding: utf-8 -*-

from base import BaseHandler
from api.consts.const import undefined
from api.utils.todo import Todo


class TodoHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, todo_id=None):
        if todo_id:
            todo = Todo.select(id=todo_id)
            return todo.to_front()
        else:
            todo_list = Todo.filter()
            return [todo.to_front() for todo in todo_list]

    @BaseHandler.ajax_base()
    def post(self):
        title = self.get_argument('title', None)
        summary = self.get_argument('summary', None)
        status = self.get_argument('status', None)
        species = self.get_argument('species', None)
        priority = self.get_argument('priority', None)
        created = self.get_argument('created', None)
        updated = self.get_argument('updated', None)
        todo = Todo.create(title=title, summary=summary, status=status, species=species, priority=priority,
                           created=created, updated=updated)
        return todo.to_front()

    @BaseHandler.ajax_base()
    def put(self, todo_id):
        title = self.get_argument('title', None)
        summary = self.get_argument('summary', None)
        status = self.get_argument('status', None)
        species = self.get_argument('species', None)
        priority = self.get_argument('priority', None)
        created = self.get_argument('created', None)
        updated = self.get_argument('updated', None)
        todo = Todo.select(id=todo_id)
        todo = todo.update(title=title, summary=summary, status=status, species=species, priority=priority,
                           created=created, updated=updated)
        return todo.to_front()

    @BaseHandler.ajax_base()
    def patch(self, todo_id):
        title = self.get_argument('title', undefined)
        summary = self.get_argument('summary', undefined)
        status = self.get_argument('status', undefined)
        species = self.get_argument('species', undefined)
        priority = self.get_argument('priority', undefined)
        created = self.get_argument('created', undefined)
        updated = self.get_argument('updated', undefined)
        todo = Todo.select(id=todo_id)
        todo = todo.update(title=title, summary=summary, status=status, species=species, priority=priority,
                           created=created, updated=updated)
        return todo.to_front()

    @BaseHandler.ajax_base()
    def delete(self, todo_id):
        todo = Todo.select(id=todo_id)
        todo.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
