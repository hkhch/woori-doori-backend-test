from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Category, CategoryItem, RecipeItem
import json

RETURN_MESSAGE = {
    "DOES_NOT_EXIST": "데이터가 존재하지 않습니다." 
}

class CategoryView(View):
  
    def get(self, request):
        try:
            categoryList = list(CategoryItem.objects.order_by('item_number').
                            select_related('category').values(
                                'item_number',
                                'name',
                                'category__name'
                            ))
            return JsonResponse({"result" : categoryList}, status=200)
        except CategoryItem.DoesNotExist:
            return JsonResponse({"message" : RETURN_MESSAGE["DOES_NOT_EXIST"]}, status=204)
   
class RecipeView(View):

    def get(self, request):
        category_item_number = int(request.GET.get("category_item_number", "0"))
        start_offset = int(request.GET.get("start_offset", "0"))
        recipe_count = int(request.GET.get("recipe_count", "1"))

        try:
            max_recipe = RecipeItem.objects.filter(category_item__item_number=category_item_number).count()
            ideal_start_index = start_offset
            start_index = max_recipe-1 if ideal_start_index > max_recipe else ideal_start_index
            ideal_last_index = start_offset + recipe_count
            last_index = max_recipe if ideal_last_index > max_recipe  else ideal_last_index

            result = list(RecipeItem.objects.filter(category_item__item_number=category_item_number).values(
                            'recipe_number',
                            'title',
                            'name',
                            'method',
                            'image',
                            'category_item__item_number',
                            'category_item__name'))[start_index:last_index]
            return JsonResponse({
                            "recipe_total" : max_recipe,
                            "result": result}, status=200) 
        except CategoryItem.DoesNotExist:
            return JsonResponse({
                            "message": RETURN_MESSAGE["DOES_NOT_EXIST"]}, status=204)

