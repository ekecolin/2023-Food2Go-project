from django.db.models import Q
from .models import *
import itertools
import random

# take in user object
# return list of product objects to recommend
def get_recommendations_for_user(user):
    # get the order for the user (get most recent)
    #most_recent_order = Order.objects.filter(user_id=user).order_by('-date_ordered').first()
    # get the products in the order
    # get the basket in the order
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    # if there is a most recent order do x
    #else get the items in their current basket
    # get the basket items for the basket
    basket_items = BasketItem.objects.filter(basket_id=basket)
    # get the products for the basket item
    product_ids = []
    for item in basket_items:
        product = item.product_id
        id = product.id
        product_ids.append(id)

    recommended_product_ids = []
    recommended_products = []
    if len(product_ids)==1:
        # only one product , what to do 
        #  query any rule containg the product id on the left hand side
        #  query where x is in the textfield e.g. "1,"  ",1" 
        id = product_ids[0]
        p_1 = "{},".format(id)
        p_2 = ",{}".format(id)
        recommendations = Recommendations.objects.filter(Q(left_hand_side__icontains=p_1) | Q(left_hand_side__icontains=p_2))
        for r in recommendations:
            recommended_product_ids.append(r.right_hand_side)
    elif len(product_ids)==2:
        query_string = "{},{}".format(product_ids[0], product_ids[1])
        recommendations = Recommendations.objects.filter(left_hand_side__icontains=query_string)
        for r in recommendations:
            recommended_product_ids.append(r.right_hand_side)
    elif len(product_ids)>2:
    # moer than 2 products what to do
        # [1,2,3]
        # [1,2], [2,3], [1,3] - nCr
        combinations = list(itertools.combinations(product_ids, 2))
        for comb in combinations:
            query_string = "{},{}".format(comb[0], comb[1])
            recommendations = Recommendations.objects.filter(left_hand_side__icontains=query_string)
            for r in recommendations:
                recommended_product_ids.append(r.right_hand_side)
    else:
        # 0 (or nmegative) products in an order - should not happen
        # pick three product at random
        all_products = list(Product.objects.all())
        random_products = random.sample(all_products, 3)

    if len(recommended_product_ids) == 0:
        all_products = list(Product.objects.all())
        recommended_products = random.sample(all_products, 3)
    else:
        recommended_products = list(Product.objects.filter(id__in=recommended_product_ids))
    return recommended_products
    