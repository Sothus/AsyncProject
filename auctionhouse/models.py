from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    def get_absoulte_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products')
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    descritpion = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ends = models.DateTimeField(auto_now_add=(date.today() + timedelta(days=7)))
    current_bidder = models.ForeignKey(User, default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absoulte_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    class Meta:
        pass

    def __str__(self):
        return self.name


class Biders(models.Model):
    product = models.ForeignKey(Product)
    users = models.ManyToManyField(User)

# Create your models here.
