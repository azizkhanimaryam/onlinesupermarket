from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from .forms import CommentForm

@login_required
def comment_page(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Assuming the user is logged in
            comment.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد، با تشکر!")  # Add success message
            return redirect('comments:comment_page')  # Correct URL name used here
    else:
        form = CommentForm()

    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'comment_page.html', {'form': form, 'comments': comments})

