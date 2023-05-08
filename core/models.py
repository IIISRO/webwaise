from django.db import models
import uuid
from django.contrib.auth.models import User


class AbstractModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Contact(AbstractModel):
    name = models.CharField('first name', max_length=15)
    email = models.EmailField('email')
    reason = models.CharField('reason', max_length=100, default='Other')
    message = models.TextField("Message")
    is_checked = models.BooleanField('is_checked', default=False)

    def __str__(self):
        return f'{self.email}==>{(self.reason)}'

class Product(AbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image=models.ImageField(upload_to="product_img",null=True,blank=True)
    name = models.CharField('name', max_length=200)
    price = models.IntegerField('price')
    desc = models.TextField('description')
    category = models.CharField(max_length=50, null=True, blank=True, choices=(
        ('webdevelopment' ,'webdevelopment'),
        ('iosapp' , 'iosapp'),
        ('androidapp' , 'androidapp'),
        ('uiux' , 'uiux'),
        ('logodesign' , 'logodesign'),
        ))
    type = models.CharField(max_length=50, null=True, blank=True, choices=(('custom' ,'custom'), ('standart' , 'standart')))
    is_active = models.BooleanField('is_active', default=True)

    def __str__(self):
        return f'{self.category}==>{self.name}'

class Order(AbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    costumer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    payed_amount = models.IntegerField('Payed amount', null=True, blank=True)
    deposit = models.IntegerField('deposit',null=True, blank=True)
    deposit_payed = models.BooleanField('deposit_payed', default=False)
    pay_access = models.BooleanField('pay_access', default=False)
    is_payed = models.BooleanField('is_payed', default=False)
    is_done = models.BooleanField('is_done', default=False)
    def __str__(self):
        return f'{self.product}==>{(self.costumer.email)}'

class OrderRequest(AbstractModel):
    costumer = models.ForeignKey(User, on_delete=models.CASCADE)
    requirements = models.TextField("Requirements")
    desc = models.TextField('Description')
    is_ordered = models.BooleanField('is ordered', default=False)
    def __str__(self):
            return f'{self.requirements }==>{(self.costumer.email)}'

class Project(AbstractModel):
    email = models.EmailField('Email')
    link = models.CharField('link', max_length=200)
    review = models.TextField('review')
    def __str__(self):
        return f'{self.email}==>{(self.link)}'

