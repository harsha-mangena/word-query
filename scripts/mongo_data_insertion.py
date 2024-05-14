import os
import django
import json
from pymongo import MongoClient
from django.utils import timezone
import sys
from django.db import transaction

sys.path.append('/Users/hmangina/Work/word-query')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordquery.settings')
django.setup()

from core.models import Word

# MongoDB setup
client = MongoClient('localhost', 27017)
db = client['word_query']
collection = db['word']

# Path to  JSON file
PATH = '/Users/hmangina/Desktop/dictionary_converted.json'


def process_entry(word, definitions):
    """Process a single dictionary entry into a format suitable for MongoDB and Django."""
    prsd_word = word.strip('\"').replace('\\', '').replace('//', '').replace("'", '')
    processed_definitions = [
        {
            'part_of_speech': definition["part_of_speech"].strip('\"').replace('\\', '').replace('//', ''),
            'definition': definition["definition"].strip('\"').replace('\\', '').replace('//', ''),
        } for definition in definitions
    ]
    return {
        'word': prsd_word,
        'definitions': processed_definitions,
        'length': len(prsd_word)
    }


@transaction.atomic
def save_to_django(processed_data):
    for i, entry in enumerate(processed_data, start=1):
        Word.objects.update_or_create(
            word=entry['word'],
            definition=entry['definitions'],
            count=0,
            length=entry['length'],
            popularity_updated_at=timezone.now()
        )
        if i % 100 == 0:
            print(f'{i} entries processed')


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
