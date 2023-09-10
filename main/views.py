from django.shortcuts import render
from .models import Oculi

name = ["Anemoculus", "Geoculus", "Electroculus", "Dendoculus", "Hydroculus"]
region = ["Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine"]
amount_collected = [0,0,0,0,0]
amount = [66, 131, 181, 271, 85]
description = ["A substance that has accumulated intense Anemo energy.",
               "A substance that has accumulated intense Geo energy.",
               "A substance that has accumulated intense Electro energy.",
               "A substance that has accumulated intense Dendro energy.", 
               "A substance that has accumulated intense Hydro energy."]

for i in range(len(name)) :
    bruh = Oculi(name=name[i], region=region[i], amount_collected=amount_collected[i],
                            amount=amount[i], description=description[i])
    bruh.save()
        
# Create your views here.
def show_main(request):

    # Iterating through the data
    
    b = Oculi.objects.all()
    context = {
        'oculus' : b
    }

    return render(request, "main.html", context)