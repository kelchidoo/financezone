try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post



def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
		
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"), 
		"titlea": "TRENDING",
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
	}
	return render(request, "post_detail.html", context)





def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),

		"title": "",
		"titlea": "TRENDING",
		"titleb": "ASIA",
		"titlec": "EUROPE",
		"titlei": "AUSTRALIA",
		"titlek": "TRAVEL",
		"titlej": "USA AND THE AMERICAS",
		"titleo": "EARN MONEY",
		"titlep": "FOREX",
		
		
		"titlel": "FOOD AND HEALTH",
		"titlen": "BUSINESS",
		"titleh": "LIFESTYLE",
		"titlef": "TECHNOLOGY",
		"titleg": "NEWS",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_list.html", context)


def post_aboutus(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		 
		"object_list": queryset,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"titlea": "TRENDING",
		"title": "ABOUT US",
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_aboutus.html", context)

def post_disclaimer(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		 
		"object_list": queryset,
		"titlea": "TRENDING",
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"title": "DISCLAIMER",
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_disclaimer.html", context)

	
def post_privacypolicy(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		 
		"object_list": queryset,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"titlea": "TRENDING",
		"title": "PRIVACY POLICY",
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_privacypolicy.html", context)



def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)



def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")



#def post_banking(request):

#	queryset = Post.objects.filter(section__icontains="Banking")
#	context = {
#		"object_list": queryset,
#		"section": "Banking"
#	}


#	return render(request, "post_banking.html", context)



def post_lifestyle(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Lifestyle"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "LIFESTYLE",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Lifestyle"
	}
	return render(request, "post_lifestyle.html", context)


def post_business(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Business"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"title": "BUSINESS",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Business"
	}
	return render(request, "post_business.html", context)

def post_life(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(main__icontains="Life"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"title": "MANAGE LIFE, MANAGE MONEY",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"main": "Life"
	}
	return render(request, "post_life.html", context)




def post_global(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(main__icontains="Global"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"title": "GLOBAL",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"main": "Global"
	}
	return render(request, "post_global.html", context)

def post_money(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(main__icontains="Money and Business"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"titlea": "TRENDING",
		"title":"MONEY AND BUSINESS",
		"page_request_var": page_request_var,
		"today": today,
		"main": "Money"
	}
	return render(request, "post_money.html", context)



def post_news(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(main__icontains="News"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		  
	
		

		"title": "NEWS",
		"titlea": "TRENDING",
		
		
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_news.html", context)

def post_forex(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Forex"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		 
		"title": "FOREX",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Forex"
	}
	return render(request, "post_forex.html", context)


def post_travel(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		  
		"object_list":  queryset_list.filter(section__icontains="Travel"),
		
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		 
		
		

		"title": "TRAVEL",
		"titlea": "TRENDING",
		"titleb": "ASIA",
		"titlec": "EUROPE",
		"titlei": "AUSTRALIA",
		"titlek": "RECENT POSTS",
		"titlej": "USA AND THE AMERICAS",
		"titleo": "EARN MONEY",
		"titlep": "FOREX",
		
		
		"titlel": "FOOD AND HEALTH",
		"titlen": "BUSINESS",
		"titleh": "LIFESTYLE",
		"titlef": "TECHNOLOGY",
		"titleg": "NEWS",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_travel.html", context)



def post_tech(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": Post.objects.filter(section__icontains="Tech"), 
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		
		"title": "TECHNOLOGY AND INNOVATIONS",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Tech"
	}
	return render(request, "post_tech.html", context)

def post_investment(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": Post.objects.filter(section__icontains="Investment"), 
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		  
		
		"title": "INVESTMENT",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Investment"
	}
	return render(request, "post_investment.html", context)

def post_banking(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": Post.objects.filter(section__icontains="Banking"), 
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		
		"title": "BANKING",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Banking"
	}
	return render(request, "post_banking.html", context)

def post_africa(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Africa"), 
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "AFRICA: NEWS AND ECONOMY",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Africa"
	}
	return render(request, "post_africa.html", context)


def post_asia(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Asia"), 
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "ASIA: NEWS AND ECONOMY",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Asia"
	}
	return render(request, "post_asia.html", context)


def post_americas(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Americas"), 
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "THE AMERICAS: NEWS AND ECONOMY",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Americas"
	}
	return render(request, "post_americas.html", context)


def post_europe(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Europe"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		 
		"title": "EUROPE: NEWS AND ECONOMY",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Europe"
	}
	return render(request, "post_europe.html", context)

def post_australia(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Australia"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "AUSTRALIA: NEWS AND ECONOMY",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Australia"
	}
	return render(request, "post_australia.html", context)

def post_foodandhealth(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Food And Health"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "FOOD AND HEALTH",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Food And Health"
	}
	return render(request, "post_foodandhealth.html", context)

def post_us(request):
	
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Usa"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "USA: NEWS AND ECONOMY",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Usa"
	}
	return render(request, "post_us.html", context)

def post_uk(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Uk"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "UK: NEWS AND ECONOMY",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Uk"
	}
	return render(request, "post_uk.html", context)


def post_education(request):
	
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Education"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"title": "EDUCATION",
		
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Education"
	}
	return render(request, "post_education.html", context)

def post_sports(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Sports"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		
		"title": "SPORTS",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Sports"
	}
	return render(request, "post_sports.html", context)

def post_entertainment(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Entertainment"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		  
		
		"title": "ENTERTAINMENT",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Entertainment"
	}
	return render(request, "post_entertainment.html", context)

def post_earnmoney(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if not request.user.is_staff or request.user.is_superuser or request.user.is_active:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 11) # Show 25 contacts per page
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
		"object_list": queryset_list.filter(section__icontains="Earn Money"),
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		 
		 
		"title": "EARN MONEY",
		"titlea": "TRENDING",
		"page_request_var": page_request_var,
		"today": today,
		"section": "Earn"
	}
	return render(request, "post_earnmoney.html", context)


def post_detailbank(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"), 
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailbank.html", context)

def post_detailbusiness(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailbusiness.html", context)

def post_detailnews(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailnews.html", context)

def post_detailforex(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailforex.html", context)


def post_detailtravel(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailtravel.html", context)


def post_detailearnmoney(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailearnmoney.html", context)


def post_detailafrica(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailafrica.html", context)


def post_detailtech(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailtech.html", context)

def post_detailasia(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailasia.html", context)

def post_detailamericas(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailamericas.html", context)

def post_detailfoodandhealth(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailfoodandhealth.html", context)

def post_detaileurope(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detaileurope.html", context)

def post_detailaustralia(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailaustralia.html", context)

def post_detailus(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailus.html", context)

def post_detailuk(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailuk.html", context)

def post_detailearn(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailearn.html", context)

def post_detaillifestyle(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detaillifestyle.html", context)



def post_detaillife(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"), 
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detaillife.html", context)


def post_detailmoneyandbusiness(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailmoneyandbusiness.html", context)


def post_detailglobal(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailglobal.html", context)



def post_detailbanking(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"), 
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"),
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailbanking.html", context)




def post_detailinvestment(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailinvestment.html", context)


def post_detaileducation(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detaileducation.html", context)




def post_detailsports(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailsports.html", context)




def post_detailentertainment(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	queryset_list.filter(view__icontains="Trending"),
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)	
					
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments
	context = {
		"title": instance.title,
		"object_lista": queryset_list.filter(view__icontains="Trending"),
		"object_listb": queryset_list.filter(view_second__icontains="Business"), 
		"object_listc": queryset_list.filter(view_second__icontains="Banking"),  
		
		"object_listd": queryset_list.filter(view_second__icontains="Investment"),  
		"object_liste": queryset_list.filter(view_second__icontains="Earn Money"),  
		"object_listf": queryset_list.filter(view_second__icontains="Forex"),  
		"object_listg": queryset_list.filter(view_second__icontains="Africa"),
		"object_listh": queryset_list.filter(view_second__icontains="Asia"),
		"object_listi": queryset_list.filter(view_second__icontains="Americas"),
		"object_listj": queryset_list.filter(view_second__icontains="Australia"),
		"object_listk": queryset_list.filter(view_second__icontains="Europe"),
		"object_listl": queryset_list.filter(view_second__icontains="Usa"),
		"object_listm": queryset_list.filter(view_second__icontains="UK"),
		"object_listn": queryset_list.filter(view_second__icontains="Tech"),
		"object_listo": queryset_list.filter(view_second__icontains="Sports"),
		"object_listp": queryset_list.filter(view_second__icontains="Entertainment"),
		"object_listq": queryset_list.filter(view_second__icontains="Lifestyle"),
		"object_listr": queryset_list.filter(view_second__icontains="Food And Health"),
		"object_lists": queryset_list.filter(view_second__icontains="Travel"),
		"object_listt": queryset_list.filter(view_second__icontains="Education"), 
		"titlea": "TRENDING",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		
	}
	return render(request, "post_detailentertainment.html", context)









