from django.shortcuts import render, redirect
from django.conf import settings
from .forms import EntryForm
from datetime import datetime

def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data['entry']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(settings.LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f'[{timestamp}] {entry}\n')
            return redirect('/ex02/')

    form = EntryForm()
    history = []
    try:
        with open(settings.LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    history.append(line)
    except FileNotFoundError:
        pass

    return render(request, 'ex02/index.html', {'form': form, 'history': history})
