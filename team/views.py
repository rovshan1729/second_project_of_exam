from django.shortcuts import render

# Create your views here.
import aiohttp
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Employee
from .serializers import EmployeeSerializer

class GetEmployeesView(APIView):

    async def fetch_data(self):
        url = settings.EXTERNAL_SYSTEM_URL
        auth = aiohttp.BasicAuth(settings.EXTERNAL_SYSTEM_LOGIN, settings.EXTERNAL_SYSTEM_PASSWORD)
        payload = {
            "Request_id": "e1477272-88d1-4acc-8e03-7008cdedc81e",
            "ClubId": settings.CLUB_ID,
            "Method": "GetSpecialistList",
            "Parameters": {
                "ServiceId": ""
            }
        }

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.post(url, json=payload) as response:
                return await response.json()

    async def get(self, request):
        data = await self.fetch_data()
        if 'employees' not in data:
            return Response({"error": "Invalid response from external system"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        employees = data['employees']
        employee_objs = []
        for employee in employees:
            employee_obj = Employee(
                id=employee.get('id', ''),
                name=employee.get('name', ''),
                last_name=employee.get('last_name', ''),
                phone=employee.get('phone', ''),
                image_url=employee.get('image_url', '')
            )
            employee_objs.append(employee_obj)

        Employee.objects.bulk_create(employee_objs, ignore_conflicts=True)

        serializer = EmployeeSerializer(employee_objs, many=True)
        return Response(serializer.data)