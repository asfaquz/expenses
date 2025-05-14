from django.db import models

class Category(models.Model):
    """
    Category model to store category information.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name
    


class Expenses(models.Model):
    """
    Expenses model to store expense information.
    """

    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='expenses')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'expenses'

    def __str__(self):
        return f"{self.name} - {self.amount} - {self.date} - {self.category}"