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

print("Calling FindAProtest API to insert topics as categories")
for topic in topics:
    response = requests.post('https://findaprotest.herokuapp.com/api/generic/category',
            data = {
                'name': topic['name']
            })
    print(topic['name'])

print("Getting events from meetup...")

events = requests.get('https://api.meetup.com/2/open_events?and_text=False&country=us&offset=0&city=Gainesville&format=json&limited_events=False&state=fl&photo-host=public&page=500&radius=25.0&desc=False&status=upcoming&sign=true&key=' + meetup_api_key).json()

# This currently results in 500s from Dave's API...investigate
print ("Calling FindAProtest API to insert events")
for event in events['results']:
    print(event['venue'] if 'venue' in event else "Unknown")
    response = requests.post('https://findaprotest.herokuapp.com/api/generic/event',
            data = {
                'name': event['group']['name'],
                'description': event['description'] if 'description' in event else "Unknown",
                'city': event['venue']['city'] if 'venue' in event and 'city' in event['venue'] else "Gainesville",
                'state': event['venue']['state'] if 'venue' in event and 'state' in event['venue'] else "FL",
                'location': event['venue']['name'] if 'venue' in event and 'name' in event['venue'] else "Unknown",
                'summary': event['name'] if 'name' in event else "Unknown", # you can thank meetup for this confusing name field
                'eventTime': event['time'] / 1000 if 'time' in event else "Unknown",
                'createdTime': event['created'] / 1000 if 'created' in event else "Unknown",
                'updatedTime': event['updated'] / 1000 if 'updated' in event else "Unknown",
                'link': event['event_url'] if 'event_url' in event else "Unknown",
                'estimatedSize': event['yes_rsvp_count'] if 'yes_rsvp_count' in event else "Unknown",
                'actualSize': event['yes_rsvp_count'] if 'yes_rsvp_count' in event else "Unknown"
            })
    print(response.text)
    print(event['group']['name'])
