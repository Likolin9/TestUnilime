import csv

from models import Product, Review

for filename in ('Products.csv', 'Reviews.csv'):
    print(filename)
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if filename == 'Products.csv':
                row = Product.convert_row_to_columns(**row)
                Product.create(**row)
            else:
                row = Review.convert_row_to_columns(**row)
                Review.create(**row)
