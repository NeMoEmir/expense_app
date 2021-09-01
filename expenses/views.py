# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets, status
from expenses.models import Expense, Category
from expenses.serializers import ExpenseSerializer, ExpenseDetailSerializer
from users.models import Account
from .permissions import IsOwner
from rest_framework.response import Response
from .validators import TopUpValidator
from .services import TopUpService


class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permissions_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)

    def get_queryset(self):
        return Expense.objects.filter(account=self.request.user.account)


class ExpenseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class BalanceIncreaseAPIView(generics.GenericAPIView):
    validator_class = TopUpValidator
    service_class = TopUpService

    def post(self, request, *args, **kwargs):
        balance = request.data.get('balance')
        if not self.validator_class.validate_balance(request.data.get('balance')):
           return Response('Pass balance to top-up', status=status.HTTP_400_BAD_REQUEST)
        self.service_class.top_up(request.user, balance)
        return Response('Ok', status=status.HTTP_200_OK)

# class ExpenseCreateAPIView(generics.CreateAPIView):
#     serializer_class = ExpenseSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def perform_create(self, serializer):
#         serializer.save(account=self.request.user.account)
#
#
# class ExpenseListAPIView(generics.ListAPIView):
#     serializer_class = ExpenseSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get_queryset(self):
#         return Expense.objects.filter(account=self.request.user.account)
#
#
# class ExpenseRetrieveAPIView(generics.RetrieveAPIView):
#     queryset = Expense.objects.all()
#     serializer = ExpenseSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwner)
#
#
# class ExpenseUpdateAPIView(generics.UpdateAPIView):
#     queryset = Expense.objects.all()
#     serializer_class = ExpenseSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwner)
#
#
# class ExpenseDeleteAPIView(generics.DestroyAPIView):
#     queryset = Expense.objects.all()
#     serializer_class = ExpenseSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwner)

# @csrf_exempt
# @api_view(['POST'])
# def expense_create_view(request):
#     if request.method == 'POST':
#         category_id = request.POST.get('category')
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         user = request.user
#         account = Account.objects.filter(user=user).first()
#         category = Category.objects.filter(id=category_id).first()
#         expense = Expense.objects.create(
#             category=category,
#             title=title,
#             description=description,
#             price=price,
#             account=account
#         )
#
#     return HttpResponse(expense, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def expenses_list_api_view(request):
#     user = request.user
#     account = Account.objects.filter(user=user).first()
#     account_expenses = Expense.objects.filter(account=account)
#
#     serializer = ExpenseSerializer(account_expenses, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def expense_retrieve_api_view(request, pk):
#     expense = Expense.objects.filter(id=pk).first()
#
#     if expense.account != request.user:
#         return Response({"Success": False,
#                          "message": "You don't have permissions to access this object"},
#                         status=status.HTTP_403_FORBIDDEN)
#
#     serializer = ExpenseSerializer(expense)
#     return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def expense_put_update_api_view(request, pk):
#     expense = Expense.objects.filter(id=pk).first()
#     if expense.account != request.user:
#         return Response({"Success": False,
#                          "message": "You don't have permissions to access this object"},
#                         status=status.HTTP_403_FORBIDDEN)
#     print(request.data)
#
#     category = Category.objcets.filter(id=request.data.get('id')).first()
#
#     expense.category = category
#     expense.title = request.data.get('title')
#     expense.price = request.data.get('price')
#     expense.description = request.data.get('description')
#     expense.save()
#
#     return Response(data='OK', status=status.HTTP_200_OK)
#
#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def expense_delete_api_view(request, pk):
#     expense = Expense.objects.filter(id=pk).first()
#     if expense.account.user != request.user:
#         return Response({"Success": False,
#                          "message": "You don't have permission to access this object"},
#                         status=status.HTTP_403_FORBIDDEN)
#
#     expense.delete()
#     return Response('Deleted', status=status.HTTP_200_OK)