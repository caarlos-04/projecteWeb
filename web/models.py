from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('FIC', 'Fiction'),
        ('NON', 'Non-Fiction'),
        ('EDU', 'Educational'),
        ('CHI', 'Children'),
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    co_authors = models.ManyToManyField(Author, related_name='co_authored_books', blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publication_date = models.DateField()
    page_count = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'reviewer_name']

    def __str__(self):
        return f"Review for {self.book.title} by {self.reviewer_name}"

# For more info on how to use Django model fields: 
# https://docs.djangoproject.com/en/stable/ref/models/fields/
