from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ("respondent", "Респондент"),
    ("admin", "Администратор данных"),
    ("provider", "Поставщик"),
    ("support", "Агент поддержки"),
)

SUPPORT_LEVEL_CHOICES = (
    (1, "L1"),
    (2, "L2"),
    (3, "L3"),
)


class User(AbstractUser):
    """Модель пользователя."""

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="respondent")
    support_level = models.PositiveSmallIntegerField(
        'Уровень поддержки',
        choices=SUPPORT_LEVEL_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Ticket(models.Model):
    """Модель заявки."""

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("resolved", "Решена"),
        ("closed", "Закрыта"),
    ]
    SUPPORT_LINE_CHOICES = [
        (1, "Первая линия"),
        (2, "Вторая линия"),
        (3, "Третья линия"),
    ]

    CATEGORY_CHOICES = (
        ("schedule", "Изменение расписания"),
        ("api_issue", "Проблема с API"),
        ("notification", "Не понимаю уведомление"),
        ("system_performance", "Система работает медленно"),
        ("response_time", "Медленный ответ техподдержки"),
        ("other", "Другое"),
    )

    subject = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new")
    description = models.TextField(blank=True)
    support_line = models.IntegerField(choices=SUPPORT_LINE_CHOICES, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    update_at = models.DateTimeField("Обновлена", auto_now=True)
    category = models.CharField(
        'Категория',
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )

    def __str__(self):
        return f"#{self.id} — {self.subject} ({self.get_support_line_display()})"


class DataSubmission(models.Model):
    """Модель для хранения данных заявки."""

    CHANNEL_CHOICES = [
        (1, "API"),
        (2, "Онлайн-ввод"),
        (3, "Оффлайн-ввод"),
    ]
    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("error", "Ошибка"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.IntegerField(choices=CHANNEL_CHOICES)
    data = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    """Модель для управления уведомлениями."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
