from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from .models import Note
import datetime
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

permission = "Private"
editpermission = "Private"
        
class Homepage(ListView):
    model = Note
    template_name = "home.html"
    
    def get_queryset(self):
        if(self.request.user.is_authenticated):
            page = self.request.GET.get('page', 1)
            if(self.request.GET.get('authorsort', '') != ''):
                filter_val = self.request.GET.get('authorsort', '')
                new_context = Note.objects.filter(
                    author=filter_val,
                ).order_by('notedate')
                paginator = Paginator(new_context, 4)
                new_context = paginator.page(page)
                return new_context
            else:
                filter_val = self.request.GET.get('search', '')
                new_context = Note.objects.filter(
                    notename__contains=filter_val,
                ).order_by('notedate')
                paginator = Paginator(new_context, 4)
                new_context = paginator.page(page)
                return new_context
        else:
            page = self.request.GET.get('page', 1)
            if(self.request.GET.get('authorsort', '') != ''):
                filter_val = self.request.GET.get('authorsort', '')
                new_context = Note.objects.filter(
                    author=filter_val,
                ).order_by('notedate').exclude(permission=0)
                paginator = Paginator(new_context, 4)
                new_context = paginator.page(page)
                return new_context
            else:
                filter_val = self.request.GET.get('search', '')
                new_context = Note.objects.filter(
                    notename__contains=filter_val,
                ).order_by('notedate').exclude(permission=0)
                paginator = Paginator(new_context, 4)
                new_context = paginator.page(page)
                return new_context

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        var1 = []
        var2 = []
        for notes in Note.objects.all():
            date = datetime.datetime.now(datetime.timezone.utc) - notes.notedate
            dateseconds = date.seconds
            days = dateseconds / 86400
            if(days < 1):
                hours = dateseconds / 3600
                if(hours < 1):
                    minutes = dateseconds / 60
                    if(minutes < 1):
                        var1.append(int(dateseconds))
                        var2.append("seconds")
                    else:
                        var1.append(int(minutes))
                        var2.append("minutes")
                else:
                    var1.append(int(hours))
                    var2.append("hours")
            else:
                var1.append(int(days))
                var2.append("days")
        context.update({'timelapsed': var1, 'days': var2})
        return context
        
class DeleteNoteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = "delete.html"
    success_url = reverse_lazy("home")
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
        
class NoteView(UserPassesTestMixin, DetailView):
    model = Note
    template_name = "note-view.html"
    
    def test_func(self):
        obj = self.get_object()
        if(obj.permission == 0):
            return obj.author == self.request.user
        elif(obj.permission == 1):
            return True
    
class EditNoteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ['notename', 'note', 'permission', 'notedate']
    template_name = "edit-note.html"
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    def get_object(self, queryset=None, per="N"):
        obj = super(EditNoteView, self).get_object(queryset=queryset)
        global editpermission
        if(per == "N"):
            if(obj.permission == 1):
                editpermission = "Public"
            elif(obj.permission == 0):
                editpermission = "Private"
        else:
            if(per == "Public"):
                editpermission = "Public"
            elif(per == "Private"):
                editpermission = "Private"
        return obj
    
    def post(self, request, *args, **kwargs):
        global editpermission
        obj = self.get_object(None,editpermission)
        if('public' in request.POST):
            if(request.POST.get("public", "") == "publicvalue"):
                editpermission = "Public"
                Note.objects.filter(pk=obj.id).update(permission=1)
        elif('private' in request.POST):
            if(request.POST.get("private", "") == "privatevalue"):
                editpermission = "Private"
                Note.objects.filter(pk=obj.id).update(permission=0)
        elif('note' in request.POST):
            if(request.user.is_authenticated):
                if(len(request.POST.get("notename", "")) < 100):
                    if(editpermission == "Private"):
                        Note.objects.filter(pk=obj.id).update(notename=request.POST.get("notename", ""),author=request.user, permission=0, note=request.POST.get("note", ""), moded=1, notedate=datetime.datetime.now())
                        return HttpResponseRedirect(reverse('home'))
                    elif(editpermission == "Public"):
                        Note.objects.filter(pk=obj.id).update(notename=request.POST.get("notename", ""),author=request.user, permission=1, note=request.POST.get("note", ""), moded=1, notedate=datetime.datetime.now())
                        return HttpResponseRedirect(reverse('home'))
        return super().post(request, *args, **kwargs)

class CreateNoteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        global permission
        return render(request,"create-note.html",{'permission': permission,})

    def post(self, request, *args, **kwargs):
        global permission
        if('private' in request.POST):
            if(request.POST.get("private", "") == "privatevalue"):
                permission = "Private"
                return render(request,"create-note.html",{'permission': permission,})
        elif('public' in request.POST):
            if(request.POST.get("public", "") == "publicvalue"):
                permission = "Public"
                return render(request,"create-note.html",{'permission': permission,})
        elif('note' in request.POST):
            if(request.user.is_authenticated):
                if(len(request.POST.get("notename", "")) < 100):
                    if(permission == "Private"):
                        Note.objects.create(notename=request.POST.get("notename", ""),author=request.user, permission=0,note=request.POST.get("note", ""))
                        return HttpResponseRedirect(reverse('home'))
                    elif(permission == "Public"):
                        Note.objects.create(notename=request.POST.get("notename", ""),author=request.user, permission=1,note=request.POST.get("note", ""))
                        return HttpResponseRedirect(reverse('home'))
        return render(request,"create-note.html",{'permission': permission,})
