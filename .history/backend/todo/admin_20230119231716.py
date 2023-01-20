from django.contrib import admin
from .models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", 'user_name', 'email', 'password']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['address1', 'address2', 'zip_code', 'city', 'state']


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['apartment_name', 'address', 'min_cost', 'max_cost', 'website_url', 'img_url']


class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'website_url', 'img_url', 'get_apartments']

    def get_apartments(self, obj):
        return obj.apartments.all()


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'overall_rating', 'review_text', 'cost_rating', 'maintainence_rating', 'quietness_rating',
                    'cleanliness_rating', 'apartment', 'created_at', 'updated_at', 'get_likes']

    def get_likes(self, obj):
        return obj.likes.all()

class SubleaseAdmin(admin.ModelAdmin):
    list_display = ['associated_apartment', 'tenant', 'price','beds','baths']


class ImportantBuildingAdmin(admin.ModelAdmin):
    list_display = ['building_name', 'address']

    def save_related(self, request, form, formsets, change):
        """
        After pressing "save", this finds the nearby apartments to the apartment building.
        Cannot override Save in ImportantBuilding to save all for ManyToMany Field, so this is admin job

        :param form: Contains Our current building we are saving

        More documentation in https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
        """
        super(ImportantBuildingAdmin, self).save_related(request, form, formsets, change)
        # if not form.instance.nearby_apartments.exists():
        apartments = Apartment.objects.all()
        form.instance.nearby_apartments.clear()
        for apartment in apartments:
            dist_val = form.instance.address.dist(apartment.address)
            print(dist_val)
            if dist_val <= 1:
                # If the distance from apartment to building is within 1 mile
                form.instance.nearby_apartments.add(apartment)



class DistanceMatrixModelAdmin(admin.ModelAdmin):
    list_display = ['important_building', 'apartment','straight_distance','walking_distance','biking_distance','driving_distance']
      

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentReview, ReviewAdmin)
admin.site.register(ApartmentSublease, SubleaseAdmin)
admin.site.register(ImportantBuilding, ImportantBuildingAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(DistanceMatrix, DistanceMatrixAdmin)
admin.site.register(DistanceMatrixModel, DistanceMatrixModelAdmin)
