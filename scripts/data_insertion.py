import json
from pymongo import MongoClient
from multiprocessing import Pool, cpu_count

PATH = '/Users/hmangina/Desktop/dictionary_converted.json'

client = MongoClient('localhost', 27017)

db = client['word_query']
collection = db['word']

collection.drop()

print("The 'word' collection has been dropped.")

db = client['word_query']
collection = db['word']

def process_text(text):
    pos_mapping = {
    "\"v. t.\"": "verb, transitive",
    "\"v. i.\"": "verb, intransitive",
    "\"n.\"": "noun",
    "\"adj.\"": "adjective",
    "\"adv.\"": "adverb",
    "\"prep.\"": "preposition",
    "\"conj.\"": "conjunction",
    "\"interj.\"": "interjection",
}
   
    for abb, full_form in pos_mapping.items():
        text = text.replace(abb, full_form)
    return text.strip('\"')

def process_data_chunk(chunk):
    processed_chunk = []
    for entry in chunk: 
        word = entry['word']
        definitions = entry['definitions']
        processed_definitions = []
        for definition in definitions:
            try:
                processed_pos = process_text(definition.get('part_of_speech', ''))
                processed_def = process_text(definition.get('definition', ''))
                processed_definitions.append({'part_of_speech': processed_pos, 'definition': processed_def})
            except:
                print(f"Unexpected type for definition: {type(definition)}")
        processed_chunk.append({'word': word, 'definitions': processed_definitions})
    return processed_chunk

def insert_into_mongo(processed_data):
    if processed_data:
        result = collection.insert_many(processed_data)
        print(f"Inserted {len(result.inserted_ids)} documents.")


with open(PATH, 'r') as file:
    data = json.load(file)

if isinstance(data, dict):
    data = [{'word': word, 'definitions': definitions} for word, definitions in data.items()]

def split_data_into_chunks(data_list, num_chunks):
    chunk_size = max(1, len(data_list) // num_chunks)
    return [data_list[i:i + chunk_size] for i in range(0, len(data_list), chunk_size)]

num_chunks = cpu_count()

chunk_size = len(data) // num_chunks

data_chunks = split_data_into_chunks(data, num_chunks)

if __name__ == '__main__':
    pool = Pool(processes=num_chunks)
    processed_chunks = pool.map(process_data_chunk, data_chunks)

    for processed_data in processed_chunks:
        insert_into_mongo(processed_data)

    print("Data insertion completed.")
