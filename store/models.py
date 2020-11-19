from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name= models.CharField(max_length=250, unique=True)
    slug=models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category',blank=True)
    class Meta:
        ordering =('name',)
        verbose_name='category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product', blank=True)
    price= models.DecimalField(max_digits=10,decimal_places=2)
    stock= models.IntegerField()
    available =models.BooleanField(default=True)
    created =models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)
    class Meta:
        ordering =('name',)
        verbose_name='product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name
    @property
    def image_url(self):
        if self.image and hasattr(self.image ,'url'):
            return self.image.url


class Cart(models.Model):
    # cart created on runtime so
    cart_id=models.CharField(max_length=250, blank=True)
    added_date= models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table= 'Cart'
        ordering= ['added_date']
    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    cart= models.ForeignKey(Cart , on_delete=models.CASCADE)
    quantity= models.IntegerField()
    active= models.BooleanField(default=True)

    class Meta:
        db_table= 'CartItem'

    def sub_total(self):
        subTotal= self.product.price * self.quantity
        return subTotal

    def __str__(self):
        return self.product + "" + self.quantity