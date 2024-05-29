from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Products(models.Model):
    ProductID = models.AutoField(primary_key=True)
    Product_name = models.CharField(max_length=100)
    Description = models.TextField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Availability = models.BooleanField(default=True)
    Image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.Product_name
