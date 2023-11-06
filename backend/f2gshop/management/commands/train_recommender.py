# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
from f2gshop.models import *
import random
import string
from efficient_apriori import apriori

# save as file called seed.py in <project>/<app>/management/commands/ (make the folders if they don't exist)
# called using python manage.py seed

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')



def train_recommender():
    """
    from efficient_apriori import apriori
transactions = [(1, 2, 4),
                ('eggs', 'bacon', 'apple'),
                ('soup', 'bacon', 'banana'),
                ('peanut butter')
                ]
    
    """
    transactions = [] 
    orders = Order.objects.all()
    for order in orders:
        # get the basket form the order
        basket = order.basket_id
        # get the basket items from the basket
        basketitems = BasketItem.objects.filter(basket_id=basket)
        product_list = []
        for basketitem in basketitems:
            # get the product id from the basket items
            pid = basketitem.product_id.id
            product_list.append(pid)
        product_tuple = tuple(product_list)
        transactions.append(product_tuple)
    itemsets, rules = apriori(transactions, min_support=0.5, min_confidence=1)
    for r in rules:
        left_side = r.lhs.replace("(","").replace(")","").replace(" ","") # string "1,2,3" = 1,2 => 3   | 2,1=>3 
        # 2 queries = 1,2 => 2,1
        lhs_2 = ','.join(left_side.split(",")[::-1])
        # save twice in db and run one query , (1,2=>3), (2,1=>3) -> only 1 query 
        right_side = int(r.rhs[0]) # the actual recommendation a foreign key to product
        r1 = Recommendations.objects.create(left_side, right_side)
        r2 = Recommendations.objects.create(lhs_2, right_side)


def run_seed(self, mode):
    """ Seed database based on mode
    :param mode: refresh / clear
    :return:
    """
    train_recommender()