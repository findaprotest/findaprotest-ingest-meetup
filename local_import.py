import os
import requests
import json
import time

if "MEETUP_API_KEY" in os.environ:
    meetup_api_key = os.environ["MEETUP_API_KEY"]
else:
    raise AttributeError('MEETUP_API_KEY is a required environment variable')

print("Getting categories from meetup api...")
categories = requests.get('https://api.meetup.com/find/topic_categories?&sign=true&photo-host=public').json()

print("Getting topics from meetup...")
topics = requests.get('https://api.meetup.com/find/topics?photo-host=public&query=protest&sign=true&key=' + meetup_api_key).json()

print("Calling FindAProtest API to insert topics")
for topic in topics:
    response = requests.post('https://findaprotest.herokuapp.com/api/generic/movement',
            data = {
                'name': topic['name'],
                'description': topic['description'],
                'date': int(time.time()),
                'link': 'https://www.meetup.com/topics/' + topic['urlkey'] + '/'
            })
    print(topic['name'])

print("Getting events from meetup...")
events = requests.get('https://api.meetup.com/2/open_events?and_text=False&country=us&offset=0&city=Gainesville&format=json&limited_events=False&state=fl&photo-host=public&page=500&radius=25.0&desc=False&status=upcoming&sign=true&key=' + meetup_api_key).json()

# This currently results in 500s from Dave's API...investigate
print ("Calling FindAProtest API to insert events")
for event in events['results']:
    response = requests.post('https://findaprotest.herokuapp.com/api/generic/event',
            data = {
                'name': event['group']['name'],
                'description': event['description'],
                'city': event['venue']['city'],
                'state': event['venue']['state'],
                'location': event['venue']['name'],
                'summary': event['name'], # you can thank meetup for this confusing name field
                'eventTime': event['time'],
                'createdTime': event['created'],
                'updatedTime': event['updated'],
                'link': event['event_url'],
                'estimatedSize': event['yes_rsvp_count'],
                'actualSize': event['yes_rsvp_count']
            })
    print(response.text)
    print(event['group']['name'])
