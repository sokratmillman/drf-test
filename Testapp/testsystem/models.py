from django.db import models


class Test(models.Model):
    num_of_questions = models.IntegerField(
        default=2, verbose_name="Количество вопросов")
    is_published = models.BooleanField(
        default=True, verbose_name="Показывать ли")
    test_name = models.CharField(max_length=100, verbose_name="Название теста")

    def __str__(self) -> str:
        return self.test_name


class Question(models.Model):
    test = models.ForeignKey(
        Test,
        related_name="questions",
        on_delete=models.CASCADE)
    question_text = models.CharField(
        max_length=200, verbose_name="Текст вопроса")
    question_type = models.CharField(
        max_length=100, choices=[
            ("MC", "Multichoice"), ("SC", "Singlechoice")], verbose_name="Тип вопроса")

    def __str__(self) -> str:
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="choices",
        on_delete=models.CASCADE)
    is_correct = models.BooleanField(
        default=False, verbose_name="Верный ответ")
    choice_text = models.CharField(max_length=200, verbose_name="Текст опции")

    def __str__(self) -> str:
        return self.choice_text


class Result(models.Model):
    username = models.CharField(max_length=100)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    result_string = models.TextField(default="")

    def __str__(self) -> str:
        return f"Результаты теста \"{self.test_name}\" пользователя {self.username}"
