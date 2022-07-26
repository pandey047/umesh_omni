from django.contrib import admin
from . models import DatabaseConnection,DataModel,DataSource,Explorer
# Register your models here.
class DatabaseConnectionAdmin(admin.ModelAdmin):
    list_display=['id','name','creationUser','creationTime','lastUpdatedUser','lastUpdateTime','parameter']

class DataModelAdmin(admin.ModelAdmin):
    list_display=['id','name','creationUser','creationTime','lastUpdatedUser','lastUpdateTime','parameter']
    
class DataSourceAdmin(admin.ModelAdmin):
    list_display=['id','name','creationUser','creationTime','lastUpdatedUser','lastUpdateTime','parameter']
    
class ExplorerAdmin(admin.ModelAdmin):
    list_display=['id','name','creationUser','creationTime','lastUpdatedUser','lastUpdateTime','parameter']
    
admin.site.register(DatabaseConnection,DatabaseConnectionAdmin)
admin.site.register(DataModel,DataModelAdmin)
admin.site.register(DataSource,DataSourceAdmin)
admin.site.register(Explorer,ExplorerAdmin)