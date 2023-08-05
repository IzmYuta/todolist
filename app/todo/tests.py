from http.cookies import SimpleCookie
from zoneinfo import ZoneInfo

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Todo


class TodoListAPIViewTest(APITestCase):
    def setUp(self):
        self.client.cookies = SimpleCookie({"uid": "test_uid"})
        self.url = reverse("todo:todo-list")
        self.todo = Todo.objects.create(title="Test Todo", uid="test_uid")

    def test_get_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.todo.id))
        self.assertEqual(response.data[0]["uid"], "test_uid")
        self.assertEqual(response.data[0]["title"], self.todo.title)
        self.assertEqual(response.data[0]["status"], self.todo.status)

    def test_get_success_correct_order(self):
        self.todo2 = Todo.objects.create(
            title="Test Todo2",
            uid="test_uid",
            deadline=timezone.datetime(2021, 1, 1, tzinfo=ZoneInfo("Asia/Tokyo")),
        )
        self.todo3 = Todo.objects.create(
            title="Test Todo3",
            uid="test_uid",
            deadline=timezone.datetime(2021, 1, 2, tzinfo=ZoneInfo("Asia/Tokyo")),
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.todo2.id))
        self.assertEqual(response.data[1]["id"], str(self.todo3.id))
        self.assertEqual(response.data[2]["id"], str(self.todo.id))

    def test_get_failure_other_person_todo(self):
        self.client.cookies = SimpleCookie({"uid": "other_uid"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data)


class TodoCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("todo:todo-list")
        self.data = {"title": "Test Todo", "deadline": "2021-01-01"}

    def test_post_success(self):
        self.client.cookies = SimpleCookie({"uid": "test_uid"})
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.filter(title="Test Todo").count(), 1)

    def test_post_success_with_no_uid(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.filter(title="Test Todo").count(), 1)


class TodoUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.client.cookies = SimpleCookie({"uid": "test_uid"})
        self.todo = Todo.objects.create(title="Test Todo", uid="test_uid")
        self.url = reverse("todo:todo-detail", kwargs={"pk": self.todo.pk})
        self.data = {"title": "Update Todo", "status": "wip", "deadline": "2021-01-01"}

    def test_put_success(self):
        response = self.client.put(self.url, self.data)
        obj = Todo.objects.get(pk=self.todo.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(obj.title, self.data["title"])
        self.assertEqual(obj.status, self.data["status"])
        self.assertEqual(
            obj.deadline, timezone.datetime(2021, 1, 1, tzinfo=ZoneInfo("Asia/Tokyo"))
        )

    def test_patch_success(self):
        response = self.client.patch(self.url, self.data)
        obj = Todo.objects.get(pk=self.todo.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(obj.title, self.data["title"])
        self.assertEqual(obj.status, self.data["status"])
        self.assertEqual(
            obj.deadline, timezone.datetime(2021, 1, 1, tzinfo=ZoneInfo("Asia/Tokyo"))
        )

    def test_put_failure_todo_not_found(self):
        self.todo.delete()
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_failure_todo_not_found(self):
        self.todo.delete()
        response = self.client.patch(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_failure_invalid_pk(self):
        self.url = reverse("todo:todo-detail", kwargs={"pk": 999})
        response = self.client.put(self.url, self.data)
        obj = Todo.objects.get(pk=self.todo.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(obj.title, self.todo.title)

    def test_patch_failure_invalid_pk(self):
        self.url = reverse("todo:todo-detail", kwargs={"pk": 999})
        response = self.client.patch(self.url, self.data)
        obj = Todo.objects.get(pk=self.todo.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(obj.title, self.todo.title)

    def test_put_failure_other_person_todo(self):
        self.client.cookies = SimpleCookie({"uid": "other_uid"})
        response = self.client.put(self.url, self.data)
        obj = Todo.objects.get(pk=self.todo.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(obj.title, self.todo.title)

    def test_patch_failure_other_person_todo(self):
        self.client.cookies = SimpleCookie({"uid": "other_uid"})
        response = self.client.put(self.url, self.data)
        obj = Todo.objects.get(pk=self.todo.pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(obj.title, self.todo.title)


class TodoDeleteAPIViewTest(APITestCase):
    def setUp(self):
        self.client.cookies = SimpleCookie({"uid": "test_uid"})
        self.todo = Todo.objects.create(title="Test Todo", uid="test_uid")
        self.url = reverse("todo:todo-detail", kwargs={"pk": self.todo.pk})

    def test_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.filter(title="Test Todo").count(), 0)

    def test_delete_failure_todo_not_found(self):
        self.todo.delete()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_failure_invalid_pk(self):
        self.url = reverse("todo:todo-detail", kwargs={"pk": 999})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Todo.objects.filter(title="Test Todo").count(), 1)

    def test_delete_failure_other_person_todo(self):
        self.client.cookies = SimpleCookie({"uid": "other_uid"})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Todo.objects.filter(title="Test Todo").count(), 1)
