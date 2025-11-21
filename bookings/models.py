from django.db import models
from datetime import date


class Booking(models.Model):
    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Номер отеля"
    )
    
    date_start = models.DateField(
        verbose_name="Дата начала",
        help_text="Дата заезда (формат: YYYY-MM-DD)"
    )
    
    date_end = models.DateField(
        verbose_name="Дата окончания",
        help_text="Дата выезда (формат: YYYY-MM-DD)"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания брони"
    )
    
    class Meta:
        db_table = "bookings_booking"
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["date_start"]
        indexes = [
            models.Index(
                fields=["room", "date_start", "date_end"],
                name="idx_bookings_room_dates"
            ),
            models.Index(
                fields=["date_start"],
                name="idx_bookings_date_start"
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_end__gt=models.F('date_start')),
                name='check_dates'
            ),
            models.CheckConstraint(
                check=models.Q(date_start__gte=date.today()),
                name='check_not_past_dates'
            ),
        ]
    
    def __str__(self):
        return f"Бронь #{self.id}: {self.room.name} ({self.date_start} - {self.date_end})"
    
    def __repr__(self):
        return (
            f"<Booking(id={self.id}, room_id={self.room_id}, "
            f"dates={self.date_start}..{self.date_end})>"
        )
    
    @property
    def duration_days(self):
        return (self.date_end - self.date_start).days
    
    @property
    def total_price(self):
        return self.room.price * self.duration_days
