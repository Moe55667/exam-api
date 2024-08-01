from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StudentReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    student_name = models.CharField(max_length=100,null=True)
    book_name = models.CharField(max_length=100,null=True)
    final_score = models.IntegerField(null=True)
    incorrect_answers_count = models.IntegerField(null=True)

class QuestionDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    student_review = models.ForeignKey(StudentReview, on_delete=models.CASCADE, related_name='detailed_review')
    question_number = models.IntegerField(null=True)
    reason = models.TextField(null=True)
    correct_answer = models.TextField(null=True)