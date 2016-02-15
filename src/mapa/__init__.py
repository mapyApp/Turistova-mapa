# -*- coding: utf-8 -*-
from models import *

print("server start NOW")

# inicializacia databazy...
default_layers = ["All"]
default_kraje = "Bratislavský, Košický, Trenčiansky, Trnavský, Prešovský, Nitriansky".split()
print(default_kraje)


layers = [ layer.name for layer in Layer.objects.all() ]

for new_layer_name in default_layers:
    if not new_layer_name in layers:
         l = Layer(name=new_layer_name)
         l.save()

print(Layer.objects.all())