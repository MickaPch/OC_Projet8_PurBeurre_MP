from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.hashers import make_password

import os
import json

class Command(BaseCommand):


    def handle(self, *args, **kwargs):

        products = [
            {
                "model": "products.Products",
                "pk": 1,
                "fields": {
                    "code": "3017620422003",
                    "name": "Nutella pate a tartiner aux noisettes et au cacao",
                    "url": "https://fr.openfoodfacts.org/produit/3017620422003/nutella-pate-a-tartiner-aux-noisettes-et-au-cacao-ferrero",
                    "quantity": "400 g",
                    "country": "France",
                    "ingredients": "Sucre, huile de palme, _noisettes_ 13%, _lait_ écrémé en poudre 8,7%, cacao maigre 7,4%, émulsifiants: lécithines [_soja_] ; vanilline. Sans gluten",
                    "energy": 2252,
                    "fat": 30.9,
                    "satured_fat": 10.6,
                    "carbohydrates": 57.5,
                    "sugar": 56.3,
                    "fibers": 0,
                    "proteins": 6.3,
                    "salt": 0.107,
                    "sodium": 0.0428,
                    "nutriscore": "E",
                    "image_url": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.248.400.jpg",
                    "compare_to_category": "en:sugary-cooking-helpers"
                }
            },
            {
                "model": "products.Categories",
                "pk": 1,
                "fields": {
                    "name": "en:sugary-cooking-helpers",
                    "name_fr": "Aide culinaire sucrée",
                    "url": "https://fr.openfoodfacts.org/categorie/aide-culinaire-sucree",
                }
            },
            {
                "model": "products.Stores",
                "pk": 1,
                "fields": {
                    "name": "Store",
                }
            },
            {
                "model": "products.Brands",
                "pk": 1,
                "fields": {
                    "name": "Brand",
                }
            },
            {
                "model": "products.ProdCat",
                "pk": 1,
                "fields": {
                    "product": "3017620422003",
                    "category": "en:sugary-cooking-helpers",
                }
            },
            {
                "model": "products.ProdStore",
                "pk": 1,
                "fields": {
                    "product": "3017620422003",
                    "store": 1,
                }
            },
            {
                "model": "products.ProdBrand",
                "pk": 1,
                "fields": {
                    "product": "3017620422003",
                    "brand": 1,
                }
            }
        ]        
        path_file = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            ),
            'fixtures',
            'products.json'
        )

        with open(path_file, 'w') as file_fixture:
            file_fixture.write(json.dumps(products))

        # call_command('loaddata', 'products')