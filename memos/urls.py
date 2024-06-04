from django.urls import path, include
from .views import Homepage, CreateNoteView, EditNoteView, NoteView, DeleteNoteView

urlpatterns = [
    path("", Homepage.as_view(), name="home"),
    path("create-note/", CreateNoteView.as_view(), name="create"),
    path("edit-note/<int:pk>/", EditNoteView.as_view(), name="edit"),
    path("view-note/<int:pk>/", NoteView.as_view(), name="view"),
    path("delete-note/<int:pk>/", DeleteNoteView.as_view(), name="delete"),
]
