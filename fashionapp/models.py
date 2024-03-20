from django.contrib.admin import models
from django.db import models
from django.contrib.auth.models import User


from django.core.validators import MaxValueValidator
STATE_CHOICES = (
    ('Andaman & Nicobar Islands','Andaman & Nicobar Island'),
    ('Andhra Pradhesh','Andhra Andhra Pradhesh'),
    ('Arunachal Pradhesh','Arunachal Pradesh'),
    ('Assam','Asaam'),
    ('Bihar','Bihar'),
    ('Chandhigarh','Chandighrh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradhesh','Himachal Pradhesh'),
    ('maharastra','maharastra'),
    ('Meghalaya','Meghalaya'),
    ('Nagaland','Nagaland'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)


    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES =(
    ('S','Shoes'),

)


class Product(models.Model):
    title= models.CharField(max_length=100)
    selling_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField( choices=CATEGORY_CHOICES,
                                 max_length=2)
    product_image = models.ImageField(upload_to='production')


    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

STATUS_CHOICES =(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('on the way','on the way'),
    ('Delivered','Delivered'),
    ('Cancle','Cancle')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price












