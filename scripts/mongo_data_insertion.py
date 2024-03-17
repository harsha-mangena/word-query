import os
import django
import json
from pymongo import MongoClient
from django.utils import timezone
import sys

# Setup Django environment
sys.path.append('/Users/hmangina/Work/word-query')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordquery.settings')
django.setup()

from core.models import Word

# MongoDB setup
client = MongoClient('localhost', 27017)
db = client['word_query']
collection = db['word']

# Path to your JSON file
PATH = '/Users/hmangina/Desktop/dictionary_converted.json'

def process_entry(word, definitions):
    """Process a single dictionary entry into a format suitable for MongoDB and Django."""
    processed_definitions = [
        {
            'part_of_speech': definition["part_of_speech"].strip('\"'),
            'definition': definition["definition"].strip('\"')
        }
        for definition in definitions
    ]
    return {
        'word': word,
        'definitions': processed_definitions
    }
def save_to_django(processed_data):
    i = 0
    for entry in processed_data:
        i += 1
        print(f'{i} Done'.format(i))
        definitions_str = json.dumps(entry['definitions'])
        word_instance = Word(
            word=entry['word'].replace('\\', '').replace('//',''),
            definition=definitions_str.replace('\\', '').replace('//','') ,
            count=0,
            popularity_updated_at=timezone.now()
        )
        word_instance.save()


if __name__ == '__main__':
    # Load JSON data
    with open(PATH, 'r') as file:
        data = json.load(file)

    processed_data = [process_entry(word, definitions) for word, definitions in data.items()]

    # Insert into MongoDB
    collection.insert_many(processed_data)
    print(f"Inserted {len(processed_data)} documents into MongoDB.")

    # Save to Django
    save_to_django(processed_data)
    print("Saved data to Django.")
