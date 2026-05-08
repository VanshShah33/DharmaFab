from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300)
    description = models.TextField()
    logo = models.ImageField(upload_to='company/')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.FloatField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Manufacturing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='manufacturing/')

    def __str__(self):
        return self.title


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=80, blank=True)
    quantity = models.CharField(max_length=80, blank=True)
    message = models.TextField()
    consent = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject or 'Inquiry'}"


class Inquiry(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    fabric_name = models.CharField(max_length=200, blank=True)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15)
    quantity = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.product.name if self.product else self.fabric_name or 'General fabric'
        return f"{self.customer_name} - {target}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
