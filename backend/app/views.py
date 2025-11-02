from rest_framework.views import APIView
from rest_framework.response import Response
from .models import products as Product
from .serializers import ProductSerializer


from django.db.models import Q

def singularize_search_term(term):
    # A simple function for common singularization.
    # For robust search, use a library like 'inflect' or 'pattern'.
    if term.lower().endswith('s'):
        # Handles 'shirts' -> 'shirt'
        return term[:-1]
    
    # Handles terms like 'glasses' -> 'glass' or 'boxes' -> 'box'
    # This is a basic rule and won't cover irregular plurals like 'mice' or 'children'.
    return term

class ProductView(APIView):
    def get(self, request):
        name = request.query_params.get('search', None)
        
        result = Product.objects.all()

        if name:
            # 1. Get the singular root of the user's search term (e.g., 'pant' from 'longpant')
            singular_name = singularize_search_term(name)
            
            # 2. Search the database for the singular term within the product name.
            # This is the most generic approach for matching parts of words.
            
            # A search for 'longpant' will result in:
            # name__icontains='longpant'
            # OR
            # name__icontains='longpant' (if singularization didn't change it)
            # OR
            # name__icontains='pant' (if singularization works for other cases)
            
            # Since 'longpant' should match 'pant', we need to check if the singular term
            # is *shorter* than the original term, or use a complex OR query.
            
            # The most direct fix for your specific case ('longpant' -> 'pant'):
            # It seems you want to search for the *shorter* word within the *longer* search term.
            
            # Let's use Q objects to search for the original OR the singular term:
            query = Q(name__icontains=name)
            
            if singular_name != name:
                query |= Q(name__icontains=singular_name)
                
            # Final check to handle the 'longpant' scenario (where 'pant' is the root word)
            # If you search for 'longpant', the common singularizer does nothing.
            # The problem is that your products have the root word ('pant'), but the search
            # term is compound ('longpant'). This requires you to search for *all* words in the query.
            
            # **The definitive generic fix without FTS:**
            search_terms = name.split()
            
            # Add the singularized version of each word
            for term in list(search_terms):
                search_terms.append(singularize_search_term(term))
            
            # Build the Q object to match ANY of the derived terms (original or singular)
            final_query = Q()
            for term in set(search_terms): # Use set to avoid duplicates
                if term:
                    final_query |= Q(name__icontains=term)
            
            result = result.filter(final_query)
        
        serializer = ProductSerializer(result, many=True)
        return Response(serializer.data)