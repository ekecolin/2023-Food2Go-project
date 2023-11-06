# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
from f2gshop.models import *
import random
import string

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


"""
Generate random string of length 8
"""
def generate_random_string():
    letters = string.ascii_lowercase #['a,b'.....'z']
    return ''.join([random.choice(letters) for x in range(0,7)]) # return random string 8 characters long


def create_data():
    # create a bunch of users
    userpass = 'testing123456'
    # created the id products 
    types = {
        'lose':['1', '2', '3', '4', '13', '14', '15', '16', '25', '26', '27', '28'],# ids of products for weight loss
        'maintain':['5', '6', '7', '8', '17', '18', '19', '20', '29', '30', '31', '32'],# ids of products for stay lean
        'gain':['9', '10', '11', '12', '21', '22', '23', '24', '33', '34', '35', '36'],# ids of procuts for bulking
    }
    for t in types:
        product_list = types[t]
        for i in range(0,1000):
            # create a user object
            # generate random username and email
            uname = generate_random_string()
            uemail = "{}@test.com".format(uname)
            u = APIUser.objects.create_user(uname, userpass, uemail)
            # create basket for each user
            ubasket = Basket.objects.create(user_id=u)
            # add products to the basket
            random_products = random.sample(product_list, 3) # get three random product ids
            for ran in random_products:
                # load the product
                prod = Product.objects.get(id=ran) # load the product
                bi = BasketItem.objects.create(basket_id = ubasket, product_id=prod)
            # create an order for the user
            order = Order.objects.create(basket_id=ubasket,user_id=u)


def populate_something_else():
    ## some code to create or delete another model
    pass

def run_seed(self, mode):
    """ Seed database based on mode
    :param mode: refresh / clear
    :return:
    """
    create_data()