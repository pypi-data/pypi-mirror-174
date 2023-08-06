from datetime import datetime
import random
from django.test import TestCase

from django.urls import reverse
from django.utils import timezone

from todo_app.models import ToDoItem, ToDoList


class ToDoListTest(TestCase):
    def create_todo_list(self, title="test_for_todolist"):
        return ToDoList.objects.create(title=title + str(random.random()))


class ToDoItemTest(TestCase):
    def create_todo_item(self, title="only a test", body="yes, this is only a test"):
        list = ToDoList.objects.create(title="title_for_todoitem" + str(random.random()))
        return ToDoItem.objects.create(title=title + str(random.random()), description=body, due_date=timezone.now(),
                                       todo_list=list)

    def test_todo_item_creation(self):
        w = self.create_todo_item()
        self.assertTrue(isinstance(w, ToDoItem))
        self.assertTrue(isinstance(w.due_date, datetime))
        self.assertTrue(isinstance(w.todo_list, ToDoList))

    def test_todo_item_view(self):
        w = self.create_todo_item()
        url = reverse("index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
