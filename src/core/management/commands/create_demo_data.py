from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import DataSubmission, Ticket

User = get_user_model()


class Command(BaseCommand):
    """Демо-данные для демонстрации системы"""
    help = "Создаёт демо-данные для демонстрации системы"

    def handle(self, *args, **kwargs):
        # Удаление старых пользователей
        User.objects.filter(username__in=[
            'resp1', 'resp2', 'admin1', 'prov1', 'l1', 'l2', 'l3'
        ]).delete()

        # Создаем пользователей
        self.stdout.write("Создание пользователей")

        resp1 = User.objects.create_user(username='resp1', password='123', role='respondent')
        resp2 = User.objects.create_user(username='resp2', password='123', role='respondent')
        admin1 = User.objects.create_user(username='admin1', password='123', role='admin')
        prov1 = User.objects.create_user(username='prov1', password='123', role='provider')
        l1 = User.objects.create_user(username='l1', password='123', role='support', support_level=1)
        l2 = User.objects.create_user(username='l2', password='123', role='support', support_level=2)
        l3 = User.objects.create_user(username='l3', password='123', role='support', support_level=3)

        # Тесты по 3 каналам
        self.stdout.write("Создаём данные по 3 каналам")

        # Канал 1: API (поставщик)
        DataSubmission.objects.create(
            provider_name="prov1",
            channel=1,
            data={"student_id": 101, "score": 85},
            status="accepted"
        )

        # Канал 2: Онлайн (респондент)
        DataSubmission.objects.create(
            user=resp1,
            channel=2,
            data={"student_id": 102, "course": "Math"},
            status="accepted"
        )

        # Канал 3: Оффлайн (респондент)
        DataSubmission.objects.create(
            user=resp2,
            channel=3,
            data={"student_id": 103, "hours": 48},
            status="accepted"
        )

        # Заявки разных типов
        self.stdout.write("Создаём заявки")

         # Заявка: "API был недоступен" → эскалируется в L2
        Ticket.objects.create(
            subject="API был недоступен 10:00–11:00",
            description="Потеряно 5 пакетов данных",
            user=prov1,
            support_line=2,
            status="escalated",
            category="api_issue"
        )

        # Заявка: "Не понимаю уведомление" → L1
        Ticket.objects.create(
            subject="Почему мне пришло уведомление об ошибке?",
            description="Данные отправил корректно",
            user=resp1,
            support_line=1,
            status="open",
            category="notification"
        )

        # Заявка: "Система работает медленно" → L3
        Ticket.objects.create(
            subject="Система тормозит при загрузке",
            description="Загрузка файла занимает >2 минуты",
            user=admin1,
            support_line=3,
            status="open",
            category="system_performance"
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Демо-данные созданы!\n"
                "Логины:\n"
                "  Респонденты: resp1, resp2 / пароль: 123\n"
                "  Админ: admin1 / пароль: 123\n"
                "  Поставщик: prov1 / пароль: 123\n"
                "  L1: l1 / пароль: 123\n"
                "  L2: l2 / пароль: 123\n"
                "  L3: l3 / пароль: 123"
            )
        )
