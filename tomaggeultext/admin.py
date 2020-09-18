from django.contrib import admin

from .models import TMSeries, TMText, Comment, Delivery, Paid_subscription, Subscription

admin.site.register(TMSeries)
admin.site.register(TMText)
admin.site.register(Comment)
admin.site.register(Delivery)
admin.site.register(Paid_subscription)
admin.site.register(Subscription)