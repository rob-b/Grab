def resave(request, queryset):
    """Trigget the save method on all objects"""
    for obj in queryset:
        obj.save()
resave.short_description = 'Resave selected items'
