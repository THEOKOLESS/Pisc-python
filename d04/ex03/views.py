from django.shortcuts import render

def index(request):
    rows = []
    for i in range(50):
        shade = int(i * 255 / 49)
        rows.append({
            'black': f'rgb({shade},{shade},{shade})',
            'red':   f'rgb({shade},0,0)',
            'blue':  f'rgb(0,0,{shade})',
            'green': f'rgb(0,{shade},0)',
        })
    return render(request, 'ex03/index.html', {'rows': rows})
