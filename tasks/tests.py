
# Create your tests here.
from django.test import TestCase
from .models import Task
from .services import increment_steps, progress_percent

class TaskTest(TestCase):
    def test_progress(self):
        t = Task.objects.create(title='t', total_steps=4, completed_steps=1)
        p = progress_percent(t)
        self.assertEqual(p, 25)
        t = increment_steps(t, 2)
        self.assertEqual(t.completed_steps, 3)