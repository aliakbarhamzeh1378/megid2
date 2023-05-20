import json

json_data = '''
{
    "S003": [
            {
                "content": "temp",
                "operator": "<",
                "value": 2,
                "status": "and"
            },
            {
                "content": "temp",
                "operator": ">",
                "value": 10,
                "status": "and"

            }

        ]
}
'''

data = json.loads(json_data)

generated_code = "import redis \nr = redis.Redis() \n"
first_time = True
conditions = data['S003']['conditions']
task = data['S003']['task']
num_conditions = len(conditions)
sensors = []
condition_generate = ""
for i, condition in enumerate(conditions):
    content = condition['content']
    operator = condition['operator']
    value = condition['value']
    status = condition['status']
    if content not in sensors:
        sensors.append(content)

    if i < num_conditions - 1:
        condition_code = f"({content} {operator} {value}) {status}"
    else:
        condition_code = f"({content} {operator} {value})"

    condition_generate += condition_code

for i in sensors:
    generated_code += f"{i} =int(r.get('{i}'))\n"
generated_code += f'if {condition_generate}'
generated_code += ' : \n \t '


print(generated_code)
