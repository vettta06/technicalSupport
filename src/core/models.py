from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError

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

    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default="respondent"
                            )
    support_level = models.PositiveSmallIntegerField(
        "Уровень поддержки",
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
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default="new"
                              )
    description = models.TextField(blank=True)
    support_line = models.IntegerField(choices=SUPPORT_LINE_CHOICES, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    update_at = models.DateTimeField("Обновлена", auto_now=True)
    category = models.CharField(
        "Категория", max_length=20, choices=CATEGORY_CHOICES, default="other"
    )

    def __str__(self):
        return (
            f"#{self.id} — {self.subject} ({self.get_support_line_display()})"
        )


class DataSubmission(models.Model):
    """Модель для хранения данных заявки."""

    CHANNEL_CHOICES = [
        (1, "API"),
        (2, "Онлайн-ввод"),
        (3, "Оффлайн-ввод"),
    ]
    STATUS_CHOICES = [
        ("pending", "Ожидает валидации"),
        ("accepted", "Принято"),
        ("rejected", "Отклонено"),
    ]
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True
                             )
    provider_name = models.CharField("Имя поставщика",
                                     max_length=255,
                                     blank=True
                                     )
    channel = models.IntegerField(choices=CHANNEL_CHOICES)
    data = models.JSONField(blank=True, null=True)
    file_upload = models.FileField(upload_to="submissions/",
                                   null=True,
                                   blank=True
                                   )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField("Причина отклонения", blank=True)
    validation_errors = models.JSONField("Ошибки валидации",
                                         default=dict,
                                         blank=True
                                         )

    def clean(self):
        """Корректность"""
        if self.channel in [1, 2]:
            if not self.data:
                raise ValidationError("Поле 'data' обязательно.")
            if not isinstance(self.data, dict):
                raise ValidationError("Поле 'data' должно быть объектом.")

            if "name" not in self.data:
                self.validation_errors = {"name": "Обязательное поле"}
            else:
                self.validation_errors = {}
        elif self.channel == 3:
            self.validation_errors = {}

    def save(self, *args, **kwargs):
        """Сохранение"""
        self.full_clean()
        if self.validation_errors:
            self.status = "rejected"
        else:
            self.status = "accepted"
        super().save(*args, **kwargs)


class Notification(models.Model):
    """Модель для управления уведомлениями."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
