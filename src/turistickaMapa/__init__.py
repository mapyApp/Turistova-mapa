# -*- coding: utf-8 -*-
from mapa.models import *
from settings import *
print("server start NOW")

# inicializacia databazy...

layers = [ layer.name for layer in Layer.objects.all() ]
regions = [ region.name for region in Region.objects.all() ]

for new_layer_name in default_layers:
    if not new_layer_name in layers:
         l = Layer(name=new_layer_name)
         l.save()
for new_region_name in default_regions:
    if not new_region_name in regions:
         r = Region(name=new_region_name)
         r.save()