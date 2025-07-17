from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ImageUploadForm, UserRegisterForm
from .models import TranslatedImage
from .services import process_image_translation


def register_view(request):
    if request.user.is_authenticated:
        return redirect("translator:translate")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Реєстрація успішна! Вітаємо, {user.username}!")
            return redirect("translator:translate")
    else:
        form = UserRegisterForm()
    return render(request, "translator/register.html", {"form": form})


@login_required
def translate_view(request):
    form = ImageUploadForm(request.POST or None, request.FILES or None)
    context = {"form": form}

    if request.method == "POST":
        if form.is_valid():
            image_file = form.cleaned_data["image"]
            target_language = form.cleaned_data["language"]
            try:

                result_record = process_image_translation(image_file, target_language, user=request.user)
                context["submitted"] = True
                context["result_record"] = result_record
            except Exception as e:
                context["error"] = f"Сталася помилка: {e}"

    return render(request, "translator/translate.html", context)


@login_required
def download_file_view(request, record_id, file_type):
    record = get_object_or_404(TranslatedImage, pk=record_id, user=request.user)

    file_to_serve = None
    if file_type == "original_text":
        file_to_serve = record.original_text_file
    elif file_type == "translated_text":
        file_to_serve = record.translated_text_file

    if file_to_serve:
        response = FileResponse(file_to_serve.open("rb"), as_attachment=True)
        return response
    else:
        raise Http404("Тип файлу не знайдено.")


@login_required
def history_view(request):
    records = TranslatedImage.objects.filter(user=request.user).order_by("-created_at")
    context = {"records": records}
    return render(request, "translator/history.html", context)


@login_required
def result_detail_view(request, record_id):
    record = get_object_or_404(TranslatedImage, pk=record_id, user=request.user)
    form = ImageUploadForm(initial={"language": record.target_language})

    context = {"form": form, "submitted": True, "result_record": record}
    return render(request, "translator/translate.html", context)


@login_required
def delete_record_view(request, record_id):
    if request.method == "POST":
        record = get_object_or_404(TranslatedImage, pk=record_id, user=request.user)

        record.original_image.delete(save=False)
        record.translated_image.delete(save=False)
        record.original_text_file.delete(save=False)
        record.translated_text_file.delete(save=False)

        record.delete()

        return redirect("translator:history")

    return redirect("translator:history")
