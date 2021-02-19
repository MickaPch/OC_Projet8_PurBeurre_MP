from django.core.management.base import BaseCommand

from products.management.commands.functions import list_products, truncate_table
from products.management.commands.classes import ImportCategories, ProductImportation, DatabaseCount, Category
from products.models import Categories, Products

from tqdm import tqdm
import datetime

class Command(BaseCommand):
    """Import datas"""

    def handle(self, *args, **kwargs):
        """LLL"""

        start = datetime.datetime.now()

        print('Truncate tables')

        tables = [
            'products_products',
            'products_categories',
            'products_relatedcategories',
            'products_prodcat',
            'products_stores',
            'products_prodstore',
            'products_brands',
            'products_prodbrand',
        ]

        for table in tables:
            truncate_table(table)
        print('Import datas')

        categories = ImportCategories()

        print(
            '{} categories imported...'.format(
                categories.all.count()
            )
        )

        print(
            '{} lines in DB'.format(
                DatabaseCount.count
            )
        )

        i = 0
        # while (
        #     i < categories.all.count()
        #     and DatabaseCount.count < 9000
        # ):
        pbar = tqdm(
            categories.all,
            position=0,
            leave=True,
            desc='Categories progress'
        )
        for category_object in pbar:
            printable_variables = {
                '': category_object.name,
                'products': ProductImportation.count,
                'lines': DatabaseCount.count
            }
            pbar.postfix=(printable_variables)
            # print('Actual category : ', category_object)
            # print('NB products in DB : ', ProductImportation.count)
            # print('NB lines : ', DatabaseCount.count)

            # category = Category(categories.all[i])

            # i += 1
            if DatabaseCount.count < 9000:
                category = Category(category_object)
                # TO INCLUDE IN WHILE LOOP
                # products = category.get_products_list()
                products = category.get_products_list(pages=5)

                # import pdb; pdb.set_trace()

                for product in products:
                    if DatabaseCount.count < 9000:
                        new_product = ProductImportation(product)
                # TO INCLUDE IN WHILE LOOP

        print('NB products in DB : ', ProductImportation.count)
        print('NB lines : ', DatabaseCount.count)
        time_import = datetime.datetime.now() - start
        print('Time delta = ', str(time_import))

