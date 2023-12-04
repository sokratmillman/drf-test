from rest_framework import status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Result, Test
from .serializers import (DashboardTestSerializer, ResultSerializer,
                          TestSerializer)
from .utils import get_result_string


class Dashboard(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user
        available_tests = Test.objects.filter(is_published=True).exclude(
            result__username=username).only('test_name')
        passed_tests = Result.objects.filter(
            username=username).only('test_id', 'test_name')
        result_list = []
        for test in available_tests:
            test_obj = {
                "id": test.id,
                "is_available": True,
                "test_name": test.test_name
            }
            result_list.append(test_obj)
        for test in passed_tests:
            test_obj = {
                "id": test.test_id.id,
                "is_available": False,
                "test_name": test.test_name
            }
            result_list.append(test_obj)
        test_serializer = DashboardTestSerializer(result_list, many=True)
        res = {"status": status.HTTP_200_OK, "data": test_serializer.data}
        return Response(res, status=status.HTTP_200_OK)


class TestView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, test_id):
        try:
            username = request.user
            if (Result.objects.filter(username=username).filter(
                    test_id=test_id).first()):
                res = {"message": "Тест уже пройден",
                       "status": status.HTTP_423_LOCKED}
                return Response(res, status=status.HTTP_423_LOCKED)

            test = Test.objects.filter(is_published=True).get(pk=test_id)
            testserializer = TestSerializer(test)
            res = {'data': testserializer.data, 'status': status.HTTP_200_OK}
            return Response(res, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            res = {"message": "Нет такого теста среди доступных",
                   "status": status.HTTP_404_NOT_FOUND}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, test_id):
        try:
            data = request.data
            test = Test.objects.get(pk=test_id)
            username = request.user.username

            if (Result.objects.filter(username=username).filter(
                    test_id=test_id).first()):
                res = {"message": "Тест уже пройден",
                       "status": status.HTTP_423_LOCKED}
                return Response(res, status=status.HTTP_423_LOCKED)
            questions = test.questions.all()

            result = {
                "username": username,
                "test_name": test.test_name,
                "test_id": test.pk,
                'result_string': get_result_string(
                    questions_set=questions,
                    sent_data=data)}

            resultserializer = ResultSerializer(data=result)
            if resultserializer.is_valid():
                resultserializer.save()
                res = {"status": status.HTTP_201_CREATED,
                       "message": "Ответы отправлены"}
                return Response(res, status=status.HTTP_201_CREATED)
            res = {"status": status.HTTP_400_BAD_REQUEST,
                   "data": resultserializer.errors}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except Test.DoesNotExist:
            res = {"message": "Нет такого теста",
                   "status": status.HTTP_404_NOT_FOUND}
            return Response(res, status=status.HTTP_404_NOT_FOUND)


class ResultView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, test_id):
        username = request.user.username
        try:
            result = Result.objects.filter(
                username=username).get(test_id=test_id)
            resultserializer = ResultSerializer(result)
            res = {"status": status.HTTP_200_OK, "data": resultserializer.data}

            return Response(res, status=status.HTTP_200_OK)
        except Result.DoesNotExist:
            res = {"message": "Нет результатов для этого теста",
                   "status": status.HTTP_404_NOT_FOUND}
            return Response(res, status=status.HTTP_404_NOT_FOUND)
