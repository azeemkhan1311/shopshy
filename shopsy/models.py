from django.db import models

# Create your models here.


class Signup(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.first_name

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Signup.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if Signup.objects.filter(email=self.email):
            return True

        return False


class Category(models.Model):
    cat_image = models.ImageField(upload_to="uploads/category/")
    cat_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    product_name = models.CharField(max_length=100, blank=True, null=True)
    product_image = models.ImageField(upload_to="uploads/products/")
    product_price = models.IntegerField()
    product_desc = models.CharField(max_length=200, blank=True, null=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    address = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    customer = models.ForeignKey(Signup, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_name
