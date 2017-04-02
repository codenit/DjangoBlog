from urllib.parse import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
# from django.core.urlresolvers import reverse

from .models import Post
from .forms import PostForm


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
        # or
        # url = reverse('detail', kwargs={'create': post_create})
        # return HttpResponseRedirect(url)

    context = {
        'form': form
    }
    return render(request, 'posts_form.html', context)


def post_detail(request, pk=None):
    instance = get_object_or_404(Post, pk=pk)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
    }
    return render(request, 'posts_detail.html', context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if not request.user.is_staff or not request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
                        Q(title__icontains=query)|
                        Q(content__icontains =query)|
                        Q(user__first_name__contains=query)|
                        Q(user__last_name__contains=query)
                        )
    paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page

    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'objects_list': queryset,
        'title': 'List',
        'page_request_var': page_request_var,
        'today': today,
    }

    return render(request, 'posts_list.html', context)


def post_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
        # or
        # url = reverse('detail', kwargs={'pk': pk})
        # return HttpResponseRedirect(url)
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'posts_form.html', context)


def post_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, pk=pk)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts : list")
