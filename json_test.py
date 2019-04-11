import json

with open("json_sample.txt") as file: # Use file to refer to the file object

   returned_labels = file.read()
   json_data = json.loads(returned_labels)

output_string = []
for label in json_data['labelAnnotations']:
    percentage_score = int(label['score'] * 100)
    description = label['description']
    text = (f'{description} at {percentage_score} percent')
    output_string.append(text)

print(output_string)

for item in output_string[0:5]:
    print(item)
