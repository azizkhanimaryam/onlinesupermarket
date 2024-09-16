from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    producer = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="files/cover", blank=True, null=True)
    availability = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    def update_availability(self):
        total_stock = sum(stock.quantity for stock in self.stocks.all())
        self.availability = total_stock > 0
        self.save()

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='stocks')
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        # Ensure that the stock's category matches the product's category
        if self.product.category != self.category:
            raise ValueError("The category of the stock must match the category of the product.")
        super().save(*args, **kwargs)
        self.product.update_availability()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product.update_availability()


class MostSoldProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='most_sold_products')
    month = models.DateField()  # Use a DateField to specify the month
    rank = models.PositiveIntegerField()  # Rank of the product

    class Meta:
        ordering = ['rank']
        unique_together = ['product', 'month']  # Ensure uniqueness per month

    def __str__(self):
        return f'{self.product.name} - {self.month.strftime("%B %Y")}'

