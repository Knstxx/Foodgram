from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint

from users.models import User
from api.models import Tag, Ingredient


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        blank=False
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='authors')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        blank=False,
        related_name='recipes',
    )
    name = models.CharField(max_length=256,
                            null=False, blank=False)
    image = models.ImageField(upload_to='recipe_images',
                              null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        null=False, blank=False
    )
    short_link = models.CharField(unique=True, max_length=256,
                                  null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=False,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        null=False,
        related_name='tags_recipes'
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=False,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        null=False,
        related_name='ingredient_recipes'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favorite')
        ]
        verbose_name = 'Любимый рецепт пользователей'
        verbose_name_plural = 'Любимые рецепты пользователей'


class ShopCard(models.Model):
    user = models.ForeignKey(
        User,
        related_name='inshop_cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='inshop_cart',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopcart')
        ]
        verbose_name = 'Список покупок пользователей'
        verbose_name_plural = 'Списки покупок пользователей'
