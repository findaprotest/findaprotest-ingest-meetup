import os
import requests
import json

if "MEETUP_API_KEY" in os.environ:
    meetup_api_key = os.environ["MEETUP_API_KEY"]
else:
    raise AttributeError('MEETUP_API_KEY is a required environment variable')

print("Getting categories from meetup api...")
categories = requests.get('https://api.meetup.com/find/topic_categories?&sign=true&photo-host=public').json()

print("Getting topics from meetup...")
topics = requests.get('https://api.meetup.com/find/topics?photo-host=public&query=protest&sign=true&key=' + meetup_api_key).json()

print("Calling FindAProtest API to insert topics as categories")
for topic in topics:
    response = requests.post('https://findaprotest.herokuapp.com/api/generic/category',
            data = {
                'name': topic['name']
            })
    print(topic['name'])

print("Getting events from meetup...")

events = requests.get('https://api.meetup.com/find/events?&sign=true&photo-host=public&lon=-82.333445&lat=29.648591&key=' + meetup_api_key).json()

print ("Calling FindAProtest API to insert events")
for event in events:
    response = requests.post('https://findaprotest.herokuapp.com/api/generic/event',
            data = {
                'name': event['group']['name'],
                'description': event['description'] if 'description' in event else "Unknown",
                'city': event['venue']['city'] if 'venue' in event and 'city' in event['venue'] else "Gainesville",
                'state': event['venue']['state'] if 'venue' in event and 'state' in event['venue'] else "FL",
                'location': event['venue']['name'] if 'venue' in event and 'name' in event['venue'] else "Unknown",
                'summary': event['name'] if 'name' in event else "Unknown", # you can thank meetup for this confusing name field
                'link': event['event_url'] if 'event_url' in event else "Unknown",
                'estimatedSize': event['yes_rsvp_count'] if 'yes_rsvp_count' in event else "Unknown",
                'actualSize': event['yes_rsvp_count'] if 'yes_rsvp_count' in event else "Unknown"
            })
    print(event['group']['name'])
