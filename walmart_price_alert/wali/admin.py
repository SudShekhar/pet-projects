from django.contrib import admin
from wali.models import Product, Discount
from django.utils import timezone
# Register your models here.
admin.site.register(Product)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'end_date', 'discounted_cost','min_customers')
    exclude = []

    def queryset(self, request):
        qs = super(DiscountAdmin, self).queryset(request)
        return qs.filter(end_date__gte = timezone.now())

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or request.user.has_perm('add_discount'):
            return True
        else:
            return False

    has_delete_permission = has_change_permission

admin.site.register(Discount, DiscountAdmin)
