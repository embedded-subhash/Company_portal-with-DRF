from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response


class TaskStatusView(APIView):

    def get(self, request, task_id):

        task = AsyncResult(task_id)

        response_data = {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.ready() else None
        }

        return Response(response_data)