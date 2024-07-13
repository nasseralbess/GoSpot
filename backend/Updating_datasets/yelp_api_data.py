import requests, json 

for i in range(20):
    
    url = "https://api.yelp.com/v3/businesses/search?location=musuems%2C%20NYC&sort_by=best_match&limit=50&offset="
    offset = i*50
    url += offset.__str__()
    print(url)
    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    del data['region']
    data['total'] = len(data['businesses'])


    with open("data.json", "r") as input_file:
        Read_data = json.load(input_file)

    def find_business_by_id(data, business_id):
        for business in data['businesses']:
            if business['id'] == business_id:
                return 1
        return 0

    count = 0
    for bus in data['businesses']:
        if (find_business_by_id(Read_data, bus['id']) == 0):
            count+= 1
            Read_data['businesses'].append(bus)
        

    print("At iteration " + i.__str__() + " We added " + count.__str__() + " elements")
 
    Read_data['total'] = len(Read_data['businesses'])
  
    if(count < 6): 
        break
    

    with open("data.json", "w") as file_output:
        json.dump(Read_data, file_output, indent=2)


print("Now number of elements is " + len(Read_data['businesses']).__str__() )


