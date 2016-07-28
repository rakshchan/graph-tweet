from django.shortcuts import render
from .forms import UserHandle
import json
from application_only_auth import Client
import operator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pylab
from matplotlib.figure import Figure
from wordcloud import WordCloud
from django.http import HttpResponse
from urllib.parse import quote

# Create your views here.
CONSUMER_KEY = 'QjV8mWFAFl7DQ6UcRvnte0wEY'
CONSUMER_SECRET = '2D2T2veOt5M0MqfliX7sI77zSpxT1kaHJvbYSYxgw3DFChpq3O'
client = Client(CONSUMER_KEY, CONSUMER_SECRET)

def home(request):
	form = UserHandle()
	if request.method == 'POST':
		form = UserHandle(request.POST)
		if form.is_valid() :
			global client
			user_handle = form.cleaned_data['handle']
			url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count=1000'.format(user_handle)
			tweet = client.request(url)
			days = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}
			data = ""
			total = 0
			for i in tweet:
				total += 1
				text = i['text'].split()
				for word in text:
					data = data + word + " "
				created = i['created_at'].split()[0]
				days[created] += 1
			if 'make-graph' in request.POST:	
				fig=Figure()
				ax=fig.add_subplot(111)
				x = [1, 2, 3, 4, 5, 6, 7]
				y = [days['Mon'], days['Tue'], days['Wed'], days['Thu'], days['Fri'], days['Sat'], days['Sun']]
				# pylab.plot(x, y)
				# pylab.xlim(1, 7)
				# pylab.ylim(0, 100)
				# pylab.xlabel('Days of week')
				# pylab.ylabel('Number of Tweets')
				# pylab.title('Line chart of tweets')
				ax.plot(x, y)
				# plt.axis([1, 7, 0, 100])
				# f = plt.gcf
				canvas = FigureCanvasAgg(fig)    
				response = HttpResponse(content_type='image/png')
				canvas.print_png(response)
				text_in_response = "<p> TOTAL: {} </p>".format(total)
				response.write(text_in_response)
				return response
			elif 'make-word-cloud' in request.POST:
				wordcloud1 = WordCloud().generate(data)
				fig=Figure()
				ax=fig.add_subplot(111)
				ax.imshow(wordcloud1)
				ax.axis("off")
				canvas = FigureCanvasAgg(fig)    
				response = HttpResponse(content_type='image/png')
				canvas.print_png(response)
				return response
	context = {'form': form}
	return render(request, 'handle.html', context)

def transliterate(request):
	global client
	search_string = "#news hai ki nahi -ban -moon"
	url_search_string = quote(search_string)
	url = "https://api.twitter.com/1.1/search/tweets.json?q=" + url_search_string
	tweets = client.request(url)
	string_tweets = json.dumps(tweets)
	# print(string_tweets)
	list_of_tweets = []
	for i in tweets['statuses']:
		list_of_tweets.append(i['text'])
	# print (list_of_tweets)
	return render(request, 'transliterate.html', {'tweets':list_of_tweets})