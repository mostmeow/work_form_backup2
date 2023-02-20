from .models import *
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

class ClassroomResource(resources.ModelResource):
    classroom = Field(
        column_name='classroom',
        attribute ='classroom',
        widget = ForeignKeyWidget(ClassroomModel, 'product_id')
    )
    channel = Field(
        column_name='channel',
        attribute ='channel',
        widget = ManyToManyWidget(ChannelModel, 'channel')
    )
    class Meta:
        model=RegisterModel