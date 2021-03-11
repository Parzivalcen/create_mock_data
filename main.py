import pandas as pd
import numpy 
import random
import datetime
import calendar

products = {
    # product:price, weights
  'iPhone': [700, 10],
  'Google Phone': [600, 8],
  'Vareebadd Phone': [400, 3],
  '20in Monitor': [109.99,6],
  '34in Ultrawide Monitor': [379.99, 9],
  '27in 4K Gaming Monitor': [389.99,9],
  '27in FHD Monitor': [149.99, 11],
  'Flatscreen TV': [300, 7],
  'Macbook Pro Laptop': [1700, 7],
  'ThinkPad Laptop': [999.99, 6],
  'AA Batteries (4-pack)': [3.84, 30],
  'AAA Batteries (4-pack)': [2.99, 30],
  'USB-C Charging Cable': [11.95, 30],
  'Lightning Charging Cable': [14.95, 30],
  'Wired Headphones': [11.99, 26],
  'Bose SoundSport Headphones': [99.99, 19],
  'Apple Airpods Headphones': [150, 22],
  'LG Washing Machine': [600.00, 1],
  'LG Dryer': [600.00, 1]
}

def generate_random_address():
    street_names = ['Main', '2nd', '1st', '4th', '5th', 'Park', '6th', '7th', 'Maple', 'Pine', 'Washington', '8th', 'Cedar', 'Elm', 'Walnut', '9th', '10th', 'Lake', 'Sunset', 'Lincoln', 'Jackson', 'Church', 'River', '11th', 'Willow', 'Jefferson', 'Center', '12th', 'North', 'Lakeview', 'Ridge', 'Hickory', 'Adams', 'Cherry', 'Highland', 'Johnson', 'South', 'Dogwood', 'West', 'Chestnut', '13th', 'Spruce', '14th', 'Wilson', 'Meadow', 'Forest', 'Hill', 'Madison']
    # all values here are in correlatives position
    cities = ['San Pedro de Y', 'Boston', 'New York City','Austin', 'Dallas', 'Atlanta', 'Portland', 'Portland', 'Los Angeles', 'Seattle']
    weights = [9,4,5,2,3,3,2,0.5,6,3]
    state = ['PY', 'MA', 'NY', 'TX', 'TX', 'GA', 'OR', 'ME', 'CA', 'WA']
    zips = ['8000', '02215', '10001', '73301', '75001', '30301', '97035', '04101', '90001', '98101']

    street = random.choice(street_names)
    index = random.choices(range(len(cities)), weights=weights)[0]

    return f"{random.randint(1,999)} {street} St, {cities[index]}, {state[index]} {zips[index]}"

def generate_random_time(month):
    # Generate a date in mm/dd/year format-H:M
        #  Number of days in a month
    day_range = calendar.monthrange(2019,month)[1]
    random_day = random.randint(1, day_range)
        # Generate the most traficc arround noon and 8pm
    if random.random() < 0.5:
        date = datetime.datetime(2019, month, random_day, 12,0)
    else:
        date = datetime.datetime(2019, month, random_day, 20,0)

    time_offset = numpy.random.normal(loc=0, scale=180)
    final_date = date + datetime.timedelta(minutes=time_offset)

    return final_date.strftime("%m/%d/%y %H:%M")

def write_row(order_id, product, order_date, address):
    # get the value for price
    price = products[product][0]
    # get quantity ordered by geometric distribution, it allows for things w/ high prices to be bought less
    quantity_ordered = numpy.random.geometric(p=1.0-(1.0/price), size=1)[0]

    return [order_id, product, quantity_ordered, price, date, address]

columns = ['Order ID', 'Product', 'Quantity Ordered', 'Price Each', 'Order Date', 'Purchase Address']

# get the keys
product_list = [product for product in products]
# grab the weight
weights = [products[product][1] for product in products]

order_id = 143253

df = pd.DataFrame(columns=columns)

for month_value in range(1,13):

    if month_value <= 10:
        # loc is our average
        orders_amount = int(numpy.random.normal(loc=3000, scale=1000))
        # orders_amount = 100

    if month_value == 11:
        #make slightly higher
        orders_amount = int(numpy.random.normal(loc=5000, scale=750))

    if month_value == 12:
        # make hight value
        orders_amount = int(numpy.random.normal(loc=6000, scale=750))

    df = pd.DataFrame(columns=columns)

    i = 0
    while orders_amount > 0:

        address = generate_random_address()
        date = generate_random_time(month_value)

        product = random.choices(product_list, weights=weights)[0]

        # add rows
        df.loc[i] = write_row(order_id, product, date, address)
        i+=1
        # add bought together products
        if product == 'iPhone':
            # 15% probability
            if random.random() < 0.15:
                df.loc[i] = write_row(order_id, 'Lightning Charging Cable', date, address)
                i+=1
            if random.random() < 0.05:
                df.loc[i] = write_row(order_id, 'Apple Airpods Headphones', date, address)
                i+=1
            if random.random() < 0.07:
                df.loc[i] = write_row(order_id, 'Wired Headphones', date, address)
                i+=1

        elif product == "Google Phone" or product == "Vareebadd Phone":
            if random.random() < 0.18:
                df.loc[i] = write_row(order_id, "USB-C Charging Cable", date, address)
                i += 1
            if random.random() < 0.04:
                df.loc[i] = write_row(order_id, "Bose SoundSport Headphones", date, address)
                i += 1

            if random.random() < 0.07:
                df.loc[i] = write_row(order_id, "Wired Headphones", date, address)
                i += 1 
        
        if random.random() <= 0.02:
            product2 = random.choices(product_list, weights=weights)[0]
            df.loc[i] = write_row(order_id, product2,date, address)
            i+=1

        order_id += 1
        orders_amount -= 1

    month_name = calendar.month_name[month_value]
    print(f'{month_name}, finished')
    df.to_csv(f'{month_name}_data.csv')
    
