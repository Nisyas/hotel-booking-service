from django.db import models


class Room(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название номера",
        help_text="Например: Двуместный люкс, Президентский сюит",
    )

    description = models.TextField(
        verbose_name="Описание удобств", help_text="Подробное описание удобств номера"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за ночь",
        help_text="Цена в рублях за одну ночь",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        db_table = "rooms_room"
        verbose_name = "Номер отеля"
        verbose_name_plural = "Номера отеля"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["price"], name="idx_rooms_price"),
            models.Index(fields=["created_at"], name="idx_rooms_created_at"),
            models.Index(fields=["name"], name="idx_rooms_name"),
        ]

    def __str__(self):
        return f"{self.name} - {self.price} ₽/ночь"

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}', price={self.price})>"
