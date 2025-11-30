from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import DataSubmission

User = get_user_model()

@api_view(['POST'])
def api_data_submission(request):
    """Канал 1: Приём данных через API."""
    provider_name = request.data.get('provider_name')
    data_payload = request.data.get('data')
    if not provider_name:
        return Response(
            {"error": "Требуется поле 'provider_name'"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not data_payload or not isinstance(data_payload, dict):
        return Response(
            {"error": "Требуется поле 'data' в виде объекта"},
            status=status.HTTP_400_BAD_REQUEST
        )
    submission = DataSubmission.objects.create(
        provider_name=provider_name,
        channel=1,
        data=data_payload,
        status='pending'
    )
    return Response(
        {
            "message": "Данные получены",
            "submission_id": submission.id,
            "status": "pending"
        },
        status=status.HTTP_201_CREATED
    )