from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	post_lifestyle,
	post_business,
	post_travel,
	
	post_tech,
	post_news,
	post_africa,
	post_americas,
	post_asia,
	post_europe,
	post_foodandhealth,
	post_australia,
	post_uk,
	post_us,
	post_forex,
	post_life,
	post_global,
	post_money,
	post_earnmoney,
	post_banking,
	post_entertainment,
	post_education,
	post_sports,
	post_investment,
	post_aboutus,
	post_disclaimer,
	post_privacypolicy,
	
	post_detailbusiness,
	post_detailsports,
	post_detaileducation,
	post_detailentertainment,
	post_detailnews,
	post_detailforex,
	post_detailtravel,
	post_detailearnmoney,
	post_detailtech,
	post_detailafrica,
	post_detailasia,
	post_detailamericas,
	post_detaileurope,
	post_detailfoodandhealth,
	post_detailaustralia,
	post_detailuk,
	post_detailearn,
	post_detaillifestyle,
	post_detailus,
	post_detailglobal,
	post_detailmoneyandbusiness,
	post_detaillife,
	post_detailbanking,
	post_detailinvestment,
	)

urlpatterns = [
	url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create),

	url(r'^business/$', post_business, name='busi'),
	url(r'^banking/$', post_banking, name='bank'),
	url(r'^investment/$', post_investment, name='inve'),
	url(r'^privacy-policy/$', post_privacypolicy, name='priv'),
	url(r'^about-us/$', post_aboutus, name='abou'),
	
	url(r'^lifestyle/$', post_lifestyle, name='lifes'),
	url(r'^education/$', post_education, name='educ'),
	url(r'^entertainment/$', post_entertainment, name='ente'),
	url(r'^disclaimer/$', post_disclaimer, name='disc'),
	url(r'^sports/$', post_sports, name='spor'),
	url(r'^africa-news-and-economy/$', post_africa, name='afri'),
	url(r'^earn-money/$', post_earnmoney, name='earn'),
	url(r'^tech/$', post_tech, name='tech'),
	url(r'^news/$', post_news, name='news'),
	url(r'^forex/$', post_forex, name='fore'),
	url(r'^travel/$', post_travel, name='trav'),
	url(r'^global/$', post_global, name='glob'),
	url(r'^money-and-business/$', post_money, name='mone'),
	url(r'^life/$', post_life, name='life'),
    url(r'^australia-news-and-economy/$', post_australia, name='aust'),
	url(r'^food-and-health/$', post_foodandhealth, name='food'),
	url(r'^europe-news-and-economy/$', post_europe, name='euro'),
	url(r'^us-news-and-economy/$', post_us, name='us'),
	url(r'^uk-news-and-economy/$', post_uk, name='uk'),
	url(r'^americas-news-and-economy/$', post_americas, name='amer'),
	url(r'^asia-news-and-economy/$', post_asia, name='asi'),
    
	url(r'^africa-news-and-economy/(?P<slug>[\w-]+)/$', post_detailafrica, name='africa'),
	url(r'^australia-news-and-economy/(?P<slug>[\w-]+)/$', post_detailaustralia, name='australia'),
	url(r'^food-and-health/(?P<slug>[\w-]+)/$', post_detailfoodandhealth, name='foodandhealth'),
	url(r'^europe-news-and-economy/(?P<slug>[\w-]+)/$', post_detaileurope, name='europe'),
	url(r'^us-news-and-economy/(?P<slug>[\w-]+)/$', post_detailus, name='usa'),
	url(r'^uk-news-and-economy/(?P<slug>[\w-]+)/$', post_detailuk, name='uking'),
	url(r'^americas-news-and-economy/(?P<slug>[\w-]+)/$', post_detailamericas, name='americas'),
	url(r'^asia-news-and-economy/(?P<slug>[\w-]+)/$', post_detailasia, name='asia'),
    
	url(r'^tech/(?P<slug>[\w-]+)/$', post_detailtech, name='technology'),
	url(r'^sports/(?P<slug>[\w-]+)/$', post_detailsports, name='sports'),
	url(r'^education/(?P<slug>[\w-]+)/$', post_detaileducation, name='education'),
	url(r'^entertainment/(?P<slug>[\w-]+)/$', post_detailentertainment, name='entertainment'),
	url(r'^global/(?P<slug>[\w-]+)/$', post_detailglobal, name='global'),
	url(r'^money-and-business/(?P<slug>[\w-]+)/$', post_detailmoneyandbusiness, name='money'),
	url(r'^life/(?P<slug>[\w-]+)/$', post_detaillife, name='lifey'),
	url(r'^news/(?P<slug>[\w-]+)/$', post_detailnews, name='news'),
    url(r'^forex/(?P<slug>[\w-]+)/$', post_detailforex, name='forex'),	
	url(r'^travel/(?P<slug>[\w-]+)/$', post_detailtravel, name='travel'),
	url(r'^earn-money/(?P<slug>[\w-]+)/$', post_detailearnmoney, name='earnmoney'),
	url(r'^lifestyle/(?P<slug>[\w-]+)/$', post_detaillifestyle, name='lifestyle'),
	url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
	
	url(r'^business/(?P<slug>[\w-]+)/$', post_detailbusiness, name='business'),
	url(r'^banking/(?P<slug>[\w-]+)/$', post_detailbanking, name='banking'),
	url(r'^investment/(?P<slug>[\w-]+)/$', post_detailinvestment, name='investment'),
	
	url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
	
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]