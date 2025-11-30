import pymysql as pql
import time


host_name = "localhost"
user_name = "root"
password = "Adit@2011"
database_name1 = 'user_details_database'
database_name2 = 'hotels_details_database'


connection_user_initial = pql.connect(host=host_name, user=user_name, password=password)
connection_hotel_initial = pql.connect(host=host_name, user=user_name, password=password)
cursor = connection_user_initial.cursor()
cursor2 = connection_user_initial.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS user_details_database')
cursor2.execute('CREATE DATABASE IF NOT EXISTS hotels_details_database')


connection_user_details = pql.connect(host=host_name, user=user_name, password=password, database=database_name1)
connection_hotel_details = pql.connect(host=host_name, user=user_name, password=password, database=database_name2)

display_item1 = """
Menu(Enter index only):
Index  Item
1      Hotel Staff Portal
2      User Portal
3      Exit
"""

display_item2 = """Hotel Portal
(Enter index only):

Index  Item
1      Add your hotel
2      View particular customer's booking
3      View your hotel's booking
4      Delete your hotel
5      Exit the portal"""

display_item3 = """User Portal
(Enter index only):

Index  Item
1      Book a hotel
2      View all the hotels
3      View particular hotel's room price
4      View your booking
5      Cancel your booking
6      Exit the portal"""

display_item4 = """Menu
(Enter index only):

Index  Item
1      Pay the amount
2      Exit (If you do so your booking will not be confirmed)
"""

def create_table1(connection_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("""
	            CREATE TABLE IF NOT EXISTS user_details (
	            name VARCHAR(255),
	            age INTEGER,
	            room_no INTEGER,
	            room_type VARCHAR(20),
	            hotel_name VARCHAR(50),
	            aadhar_no BIGINT,
	            contact_no BIGINT,
	            email_id VARCHAR(255), 
	            amount_payable FLOAT(10, 2), 
	            booking_date VARCHAR(30), 
	            booked_from VARCHAR(30),
	            booked_to VARCHAR(30), 
	            hotel_pincode INTEGER
	            )""")
	connection_obj.commit()

def create_table2(connection_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("""
	            CREATE TABLE IF NOT EXISTS hotel_details (
	            hotel_name VARCHAR(50),
	            place VARCHAR(100),
	            pin_code INTEGER, 
	            room_available INTEGER,
	            room_no VARCHAR(1200),
	            room_type1 VARCHAR(30), 
	            room_type2 VARCHAR(30), 
	            room_type3 VARCHAR(30), 
	            room_type4 VARCHAR(30), 
	            room_type1_avail INTEGER,
	            room_type2_avail INTEGER,
	            room_type3_avail INTEGER,
	            room_type4_avail INTEGER,
	            price_of_room_type1 FLOAT(10, 2),
	            price_of_room_type2 FLOAT(10, 2),
	            price_of_room_type3 FLOAT(10, 2),
	            price_of_room_type4 FLOAT(10, 2), 
	            total_booked INTEGER, 
	            contact_hotel VARCHAR(50))""")
	connection_obj.commit()

def create_hotel_rooms(rooms_avail_obj):
	room_no_obj = []
	room_no_final = []
	for floor_no in range(1, 22):
		for room_specific_no in range(0, 10):
			room_str = f"{floor_no}0{room_specific_no}"
			room_no_obj.append(int(room_str))
	return room_no_final[:rooms_avail_obj]


def enter_details(connection_obj, name_obj, age_obj, room_no_obj, room_name_obj, hotel_name_obj,
				   aadhar_no_obj, contact_no_obj, email_id_obj, amount_payable_obj, book_date_obj, booked_from_obj, booked_to_obj, pincode_obj):
	details = (name_obj, age_obj, room_no_obj, room_name_obj,
			   hotel_name_obj, aadhar_no_obj, contact_no_obj, email_id_obj,
			   amount_payable_obj,book_date_obj, booked_from_obj, booked_to_obj, pincode_obj)
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("INSERT INTO user_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", details)
	connection_obj.commit()

def enter_details2(connection_obj, hotel_name_obj, place_obj, pin_code_obj,room_available_obj,room_no_obj,
				   room_type1_obj, room_type2_obj, room_type3_obj,
				   room_type4_obj,
				   room_type1_avail_obj,room_type2_avail_obj,room_type3_avail_obj,room_type4_avail_obj,
				     price_of_room_type1_obj, price_of_room_type2_obj,
				   price_of_room_type3_obj, price_of_room_type4_obj,  total_booked_obj, contact_hotel_obj):
	details = (hotel_name_obj, place_obj, pin_code_obj, room_available_obj, room_no_obj,
			   room_type1_obj, room_type2_obj, room_type3_obj, room_type4_obj,
			   room_type1_avail_obj, room_type2_avail_obj, room_type3_avail_obj,
			   room_type4_avail_obj, price_of_room_type1_obj, price_of_room_type2_obj,
			   price_of_room_type3_obj, price_of_room_type4_obj, total_booked_obj, contact_hotel_obj)
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("INSERT INTO hotel_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", details)
	connection_obj.commit()

def query_hotel_p(connection_obj, name_obj, hotel_name_obj, pincode_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("SELECT * FROM user_details WHERE name = %s , hotel_name=%s AND hotel_pincode=%s",
					   (name_obj, hotel_name_obj, pincode_obj))
	row = cursor_obj.fetchall()
	return row

def update_hotel_no(connection_obj, room_type_obj, hotel_name_obj, pincode_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("SELECT * FROM hotel_details WHERE hotel_name=%s AND pin_code=%s", (hotel_name_obj, pincode_obj))
	row_obj = cursor_obj.fetchall()
	room_available_obj = int(row_obj[0][3]) - 1
	room_no_obj = row_obj[0][4]
	if room_type_obj == row_obj[0][5]:
		room_now_obj = row_obj[0][9] - 1
		cursor_obj.execute(
			'UPDATE hotel_details SET room_type1_avail=%s WHERE hotel_name=%s AND pin_code=%s',
			(room_now_obj,hotel_name_obj, pincode_obj))
		cursor_obj.execute(
			'UPDATE hotel_details SET room_no=%s, room_available=%s WHERE hotel_name=%s AND pin_code=%s',
			(room_no_obj,room_available_obj, hotel_name_obj, pincode_obj))
		connection_obj.commit()
	elif room_type_obj == row_obj[0][6]:
		room_now_obj = row_obj[0][10] - 1
		cursor_obj.execute(
			'UPDATE hotel_details SET room_type2_avail=%s WHERE hotel_name=%s AND pin_code=%s',
			(room_now_obj, hotel_name_obj, pincode_obj))
		cursor_obj.execute(
			'UPDATE hotel_details SET room_no=%s, room_available=%s WHERE hotel_name=%s AND pin_code=%s',
			(room_no_obj, room_available_obj, hotel_name_obj, pincode_obj))
		connection_obj.commit()
	elif room_type_obj == row_obj[0][7]:
		room_now_obj = row_obj[0][11] - 1
		cursor_obj.execute(
			'UPDATE hotel_details SET room_type3_avail=%s WHERE hotel_name=%s AND pin_code=%s',
			(room_now_obj, hotel_name_obj, pincode_obj))
		cursor_obj.execute(
			'UPDATE hotel_details SET room_no=%s, room_available=%s WHERE hotel_name=%s AND pin_code=%s',
			(room_no_obj, room_available_obj, hotel_name_obj, pincode_obj))
		connection_obj.commit()
	elif room_type_obj == row_obj[0][8]:
		room_now_obj = row_obj[0][12] - 1
		cursor_obj.execute(
			'UPDATE hotel_details SET room_type4_avail=%s WHERE hotel_name=%s AND pin_code=%s',
			(room_now_obj, hotel_name_obj, pincode_obj))
		cursor_obj.execute(
			'UPDATE hotel_details SET room_no=%s, room_available=%s WHERE hotel_name=%s AND pin_code=%s',
			(room_no_obj, room_available_obj, hotel_name_obj, pincode_obj))
		connection_obj.commit()

def get_room_no(connection_obj, hotel_name_obj, pin_code_obj):
	try:
		cursor_obj = connection_obj.cursor()
		cursor_obj.execute(
			"SELECT * FROM hotel_details WHERE hotel_name=%s AND pin_code=%s",
			(hotel_name_obj, pin_code_obj))
		row_obj = cursor_obj.fetchall()
		row_obj1 = eval(row_obj[0][4])
		row_obj2 = row_obj1[0]
		row_obj1.remove(row_obj2)
		row_obj1 = str(row_obj1)
		cursor_obj.execute('UPDATE hotel_details SET room_no=%s WHERE hotel_name=%s AND pin_code=%s', (row_obj1, hotel_name_obj, pin_code_obj))
		connection_obj.commit()
		return row_obj2
	except IndexError:
		print('\tHotel with the following name doesn\'t exist OR pincode is Incorrect')

def query_hotel(connection_obj, hotel_name_obj, pincode_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("SELECT * FROM user_details WHERE hotel_name=%s AND hotel_pincode=%s", (hotel_name_obj, pincode_obj))
	row = cursor_obj.fetchall()
	return row


def query_view_hotel(connection_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("SELECT * FROM hotel_details")
	row = cursor_obj.fetchall()
	return row

def query_hotel_price(connection_obj, hotel_name_obj, pin_code_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("SELECT room_type1, room_type1_avail, price_of_room_type1, room_type2, room_type2_avail, price_of_room_type2, room_type3, room_type3_avail, price_of_room_type3 ,room_type4, room_type4_avail, price_of_room_type4 FROM hotel_details WHERE hotel_name=%s AND pin_code=%s", (hotel_name_obj, pin_code_obj))
	row = cursor_obj.fetchall()
	return row

def query_rooms_available(connection_obj, hotel_name_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute("SELECT room_available FROM hotel_details WHERE hotel_name=%s", (hotel_name_obj, ))
	row = cursor_obj.fetchall()
	return row[0][0]

def generate_ticket(hotel_name_obj, user_name_obj,
					room_type_obj, room_no_obj, booking_date_obj, booked_from_obj, booked_to_obj, contact_obj):
	ticket_obj = f""" 
	Name: {user_name_obj.replace('_', ' ')}      Booking date:{booking_date_obj}
	Hotel Name: {hotel_name_obj.replace('_', ' ')}
	Room Type: {room_type_obj.replace('_', ' ')}
	Room No.: {room_no_obj}
		
	Booked From: {booked_from_obj}           Booked To: {booked_to_obj}
	For further information contact {contact_obj}
"""
	return ticket_obj

def delete_hotel(connection_obj, connection_obj2, hotel_name_obj, pincode_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute('DELETE FROM hotel_details WHERE hotel_name=%s AND pin_code=%s', (hotel_name_obj, pincode_obj))
	connection_obj.commit()
	cursor_obj.close()

	cursor_obj2 = connection_obj2.cursor()
	cursor_obj2.execute('DELETE FROM user_details WHERE hotel_name=%s AND hotel_pincode=%s', (hotel_name_obj, pincode_obj))
	connection_obj2.commit()
	cursor_obj2.close()

def amount_payable(connection_obj, hotel_name_obj, pincode_obj, room_type_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute(
		"SELECT * FROM hotel_details WHERE hotel_name=%s AND pin_code=%s",
		(hotel_name_obj, pincode_obj))
	row_obj = cursor_obj.fetchall()
	if room_type_obj == row_obj[0][5]:
		cursor_obj.execute('SELECT price_of_room_type1 FROM hotel_details WHERE hotel_name=%s AND pin_code=%s',(hotel_name_obj, pincode_obj))
		row_obj = cursor_obj.fetchall()
		row_obj = row_obj[0][0]
		return row_obj
	elif room_type_obj == row_obj[0][6]:
		cursor_obj.execute('SELECT price_of_room_type2 FROM hotel_details WHERE hotel_name=%s AND pin_code=%s',(hotel_name_obj, pincode_obj))
		row_obj = cursor_obj.fetchall()
		row_obj = row_obj[0][0]
		return row_obj
	elif room_type_obj == row_obj[0][7]:
		cursor_obj.execute(
			'SELECT price_of_room_type3 FROM hotel_details WHERE hotel_name=%s AND pin_code=%s',
			(hotel_name_obj, pincode_obj))
		row_obj = (cursor_obj.fetchall())
		row_obj = row_obj[0][0]
		return row_obj
	elif room_type_obj == row_obj[0][8]:
		cursor_obj.execute(
			'SELECT price_of_room_type4 FROM hotel_details WHERE hotel_name=%s AND pin_code=%s',
			(hotel_name_obj, pincode_obj))
		row_obj = cursor_obj.fetchall()
		row_obj = row_obj[0][0]
		return row_obj
#FAULTY
def delete_booking(connection_obj, connection_obj2, name_obj, hotel_name_obj, pincode_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute('SELECT room_type, room_no FROM user_details WHERE name=%s, hotel_name=%s AND hotel_pincode=%s',
					   (name_obj, hotel_name_obj, pincode_obj))
	raw_list = cursor_obj.fetchall()[0]
	cursor_obj.close()
	print(raw_list)
	room_type_obj = raw_list[0]
	room_no_obj = raw_list[1]
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute(
		"DELETE FROM user_details WHERE name=%s, hotel_name=%s AND hotel_pincode=%s",
		(name_obj, hotel_name_obj, pincode_obj))
	connection_obj.commit()
	cursor_obj.close()
	cursor_obj2 = connection_obj2.cursor()
	cursor_obj2.execute(
		'''SELECT room_type1, room_type2, room_type3, room_type4, 
		room_type1_avail, room_type2_avail, room_type3_avail, room_type4_avail, room_no,
		room_available FROM hotel_details WHERE hotel_name=%s''',
		(hotel_name_obj,))
	rooms_raw_list = cursor_obj2.fetchall()
	total_rooms_obj = rooms_raw_list[0][-1]
	total_rooms_obj = total_rooms_obj + 1
	cursor_obj2.execute(
		'UPDATE hotel_details SET room_available=%s WHERE hotel_name=%s AND pin_code=%s',
		(total_rooms_obj, hotel_name_obj, pincode_obj))
	connection_obj2.commit()
	rooms_str_list = eval(rooms_raw_list[0][-2])
	rooms_str_list.insert(int(room_no_obj), 0)
	rooms_str_list = str(rooms_str_list)
	cursor_obj2.execute(
		'UPDATE hotel_details SET room_no=%s WHERE hotel_name=%s AND pin_code=%s',
		(rooms_str_list, hotel_name_obj, pincode_obj))
	connection_obj2.commit()

	if room_type_obj == rooms_raw_list[0][0]:
		avail = rooms_raw_list[0][4] + 1
		cursor_obj2.execute(
			'UPDATE hotel_details SET room_type1_avail=%s WHERE hotel_name=%s AND pin_code=%s',
			(avail, hotel_name_obj, pincode_obj))
		connection_obj2.commit()
	elif room_type_obj == rooms_raw_list[0][1]:
		avail = rooms_raw_list[0][5] + 1
		cursor_obj2.execute(
			'UPDATE hotel_details SET room_type2_avail=%s WHERE hotel_name=%s AND pin_code=%s',
			(avail, hotel_name_obj, pincode_obj))
		connection_obj2.commit()
	elif room_type_obj == rooms_raw_list[0][2]:
		avail = rooms_raw_list[0][6] + 1
		cursor_obj2.execute(
			'UPDATE hotel_details SET room_type3_avail=%s WHERE hotel_name=%s AND pin_code=%s',
			(avail, hotel_name_obj, pincode_obj))
		connection_obj2.commit()
	elif room_type_obj == rooms_raw_list[0][3]:
		avail = rooms_raw_list[0][7] + 1
		cursor_obj2.execute(
			'UPDATE hotel_details SET room_type4_avail=%s WHERE hotel_name=%s AND pin_code=%s',
			(avail, hotel_name_obj, pincode_obj))
		connection_obj2.commit()

def authenticate_card(card_no_obj, card_holder_name_obj, exp_obj, cvv_obj):
	all_details = []
	with open('card.txt',"r") as file:
		raw_data_obj = file.readlines()
	raw_data_obj = raw_data_obj[1:]
	for i in raw_data_obj:
		expand_obj = i.strip().split(',')
		details_obj = {'card_no': int(expand_obj[0].strip()), 'holder_name':expand_obj[1].strip().upper().replace(' ', '_'),
					   'cvv': int(expand_obj[2].strip()), 'exp':expand_obj[3].strip().strip('\n')}
		all_details.append(details_obj)
	entered_details_obj = {'card_no': card_no_obj, 'holder_name':card_holder_name_obj,
					   'cvv': cvv_obj, 'exp':exp_obj}
	if entered_details_obj in all_details:
		return True
	else:
		return False

def update_amount_payable(connection_obj1, name_obj, room_no_obj, aadhar_obj):
	cursor_obj1 = connection_obj1.cursor()
	cursor_obj1.execute('UPDATE user_details SET amount_payable=0 WHERE name=%s , room_no=%s AND aadhar_no=%s',
						(name_obj, room_no_obj, aadhar_obj))
	connection_obj1.commit()


def generate_ticket_by_query(connection_obj,connection_obj1,aadhar_obj, name_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute('''SELECT name, booking_date, hotel_name, room_type, room_no, booked_from, booked_to 
	FROM user_details WHERE name=%s AND aadhar_no=%s''', (name_obj, aadhar_obj))

	try:
		raw_data_obj = cursor_obj.fetchall()[0]
		cursor_obj2 = connection_obj1.cursor()
		cursor_obj2.execute("SELECT contact_hotel FROM hotel_details WHERE hotel_name=%s", (raw_data_obj[2]))
		hotel_name_obj = cursor_obj2.fetchall()[0][0]
		ticket_obj = f""" 
	Name: {raw_data_obj[0].replace('_', ' ')}      Booking date:{raw_data_obj[1]}
	Hotel Name: {raw_data_obj[2].replace('_', ' ')}
	Room Type: {raw_data_obj[3].replace('_', ' ')}
	Room No.: {raw_data_obj[4]}
			
	Booked From: {raw_data_obj[5]}           Booked To: {raw_data_obj[6]}
	For further information contact {hotel_name_obj}
	"""
		return ticket_obj
	except IndexError:
		error_message = f'Booking with name {name_obj.replace('_', ' ')} and Aadhar {aadhar_obj} doesn\'t exist'
		return error_message

def room_booked(connection_obj, hotel_name_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute('''SELECT room_available, total_booked 
	FROM hotel_details WHERE hotel_name=%s''', (hotel_name_obj, ))
	raw_data_obj = cursor_obj.fetchall()[0]
	sum_of_rooms_obj = raw_data_obj[0]
	total_obj = raw_data_obj[1]
	difference_obj = total_obj - sum_of_rooms_obj
	return total_obj, difference_obj

def contact_no_def(connection_obj, hotel_obj, pincode_obj):
	cursor_obj = connection_obj.cursor()
	cursor_obj.execute('SELECT contact_hotel FROM hotel_details WHERE hotel_name=%s AND pin_code=%s', (hotel_obj, pincode_obj))
	result = cursor_obj.fetchall()[0][0]
	return result

def book_hotel():
	print(
		'\nHotel booked successfully')
	print('\nPayment initiated successfully')
	contact_def_no = contact_no_def(connection_hotel_details, hotel_name,
									pincode5)
	room_no = get_room_no(
		connection_hotel_details,
		hotel_name, pincode5)
	ticket = generate_ticket(hotel_name, customer_name, room_type, room_no,
							 time_now,
							 booked_from, booked_to,
							 contact_obj=contact_def_no)
	print('\n' + ticket)
	update_hotel_no(
		connection_hotel_details,
		room_type,
		hotel_name_obj=hotel_name,
		pincode_obj=pincode5)
	contact_no
	enter_details(
		connection_user_details,
		customer_name, age_obj=age,
		room_no_obj=room_no,
		hotel_name_obj=hotel_name,
		contact_no_obj=contact_no,
		email_id_obj=email_id,
		aadhar_no_obj=aadhar_no,
		room_name_obj=room_type,
		amount_payable_obj=amount,
		book_date_obj=time_now,
		booked_from_obj=booked_from,
		booked_to_obj=booked_to,
		pincode_obj=pincode5)
	update_amount_payable(
		connection_user_details,
		customer_name,
		room_no, aadhar_obj=aadhar_no)

def add_hotel():
	pincode = int(input('Enter pincode of the place: '))
	room1_name = input('Enter room 1 type: ').title().strip().replace(' ', '_')
	room2_name = input('Enter room 2 type: ').title().strip().replace(' ', '_')
	room3_name = input('Enter room 3 type: ').title().strip().replace(' ', '_')
	room4_name = input('Enter room 4 type: ').title().strip().replace(' ', '_')
	room1_avail = int(input(
		f'Enter no. of rooms available of {room1_name.replace('_', ' ')}: '))
	room2_avail = int(input(
		f'Enter no. of rooms available of {room2_name.replace('_', ' ')}: '))
	room3_avail = int(input(
		f'Enter no. of rooms available of {room3_name.replace('_', ' ')}: '))
	room4_avail = int(input(
		f'Enter no. of rooms available of {room4_name.replace('_', ' ')}: '))
	room1_price = float(
		input(f'Enter price of {room1_name.replace('_', ' ')}: '))
	room2_price = float(
		input(f'Enter price of {room2_name.replace('_', ' ')}: '))
	room3_price = float(
		input(f'Enter price of {room3_name.replace('_', ' ')}: '))
	room4_price = float(
		input(f'Enter price of {room4_name.replace('_', ' ')}: '))
	room_available = int(
		input("Enter rooms present in your hotel(Max 210): "))
	cc = input('Enter hotel\'s contact no.: ')
	sum_of_rooms = room1_avail + room2_avail + room3_avail + room4_avail
	if sum_of_rooms == room_available:
		rooms_o = create_hotel_rooms(room_available)
		rooms = len(rooms_o)
		enter_details2(connection_hotel_details,
					   hotel_name_obj=hotel_name,
					   place_obj=place,
					   pin_code_obj=pincode,
					   room_available_obj=rooms,
					   room_no_obj=str(rooms_o),
					   room_type1_obj=room1_name,
					   room_type2_obj=room2_name,
					   room_type3_obj=room3_name,
					   room_type4_obj=room4_name,
					   room_type1_avail_obj=room1_avail,
					   room_type2_avail_obj=room2_avail,
					   room_type3_avail_obj=room3_avail,
					   room_type4_avail_obj=room4_avail,
					   price_of_room_type1_obj=room1_price,
					   price_of_room_type2_obj=room2_price,
					   price_of_room_type3_obj=room3_price,
					   price_of_room_type4_obj=room4_price,
					   total_booked_obj=rooms,
					   contact_hotel_obj=cc)
		print('\nHotel added successfully!')
	else:
		print(
			'\nThe total rooms entered is not equal to sum of rooms')

# MAIN Working
create_table1(connection_user_details)
create_table2(connection_hotel_details)
print(display_item1)
while True:
	initial_choice = input('\n' + 'Enter your choice: ').strip()
	if initial_choice == '1':
		print('\n' + display_item2)
		while True:
			hotel_choice = input('\n' + 'Enter your choice(Hotel\'s Portal): ').strip()
			if hotel_choice == '1':
				print()
				hotel_name = input('Enter your hotel\'s name: ').title().strip().replace(' ', '_')
				place = input('Enter place: ').title().strip().replace(' ',
																	   '_')
				try:
					add_hotel()
				except ValueError:
					print('\nEnter an integer')
			elif hotel_choice == '2':
				name = input('Enter name of the customer: ').title().strip().replace(' ', '_')
				hotel_name = input('Enter your hotel\'s name: ').title().strip().replace(' ', '_')
				pincode1 = int(input('Enter pincode of the hotel: '))
				row1 = query_hotel_p(connection_user_details, name_obj=name, hotel_name_obj=hotel_name, pincode_obj=pincode1)
				try:
					r = row1[0][0]
					for raw_item in row1:
						final_item = f"""
	Name: {raw_item[0].replace('_', ' ')}               Age: {raw_item[1]}
	Room Number: {raw_item[2]}            Aadhar Number: {raw_item[5]}     
	Contact no.: {raw_item[6]}            Email ID: {raw_item[7]}
	Booked From: {raw_item[-2]}           Booked To: {raw_item[-1]}
	Balance Due: {raw_item[-4]}           Booking Date:{raw_item[-3]}
					"""
						print(final_item)
				except IndexError:
					print(f'\nNo booking found with name: {name.replace('_', ' ')}')
			elif hotel_choice == '3':
				hotel_name = input('Enter your hotel\'s name: ').title().strip().replace(' ', '_')
				pincode2 = int(input('Enter pincode of the hotel: '))
				row2 = query_hotel(connection_user_details, hotel_name_obj=hotel_name, pincode_obj=pincode2)
				print()
				try:
					r = row2[0][0]
					for item in row2:
						final_item1 = (f"\t{item[0].replace('_', ' ')}"
									   f"(Room No.: {item[2]},Room Type: {item[3].replace('_', ' ')}, Aadhar No.: {item[5]}, Contact No.: {item[6]}, "
									   f"Email ID: {item[7]}, \nBooked From: {item[-2]}, Booked To: {item[-1]})")
						print(final_item1 + '\n')
					total, diff = room_booked(connection_hotel_details, hotel_name_obj=hotel_name)
					print(f'Room booked: {diff}/{total}')
				except IndexError:
					print('No booking found')
			elif hotel_choice == '4':
				hotel_name = input('\nEnter hotel\'s name: ').title().strip().replace(' ',
																	   '_')
				pincode3 = int(input('Enter pincode of the hotel: '))
				delete_hotel(connection_hotel_details, hotel_name, pincode_obj=pincode3, connection_obj2=connection_user_details)
			elif hotel_choice == '5':
				print("""
Exited Hotel Portal successfully""")
				break
			else:
				print('''
Enter a valid command''')
	elif initial_choice == '2':
		choice2 = None
		print(display_item3)
		while True:
			user_choice = input('\nEnter your choice(User\'s Portal): ').strip()
			if user_choice == '1':
				choice = input('\nDo you want to see the list of hotels? ').strip().lower()
				if choice == 'yes':
					row4 = query_view_hotel(connection_hotel_details)
					try:
						row4[0][0]
						for raw_item in row4:
							final_item2 = f"""
	Hotel name: {raw_item[0].replace('_', ' ')}               Place: {raw_item[1].replace('_', ' ')}
	Pincode: {raw_item[2]}            Rooms available: {raw_item[3]}"""
							print(final_item2)
					except IndexError:
						print('\nNo hotel added yet')
					choice2 = input('\nDo you want to see particular hotel\'s room type and price? ').strip().lower()
					if choice2 == 'yes':
						hotel_name = input(
							'Enter hotel\'s name: ').title().strip().replace(' ', '_')
						pincode4 = int(input('Enter pincode of the hotel: '))
						try:
							row5 = query_hotel_price(
								connection_obj=connection_hotel_details,
								hotel_name_obj=hotel_name,
								pin_code_obj=pincode4)[0]
							row5[0]
							final_item3 = f"""
	Room Type: {row5[0].replace('_', ' ')}       Rooms available: {row5[1]}        Price of the room: {row5[2]}/-
	Room Type: {row5[3].replace('_', ' ')}       Rooms available: {row5[4]}        Price of the room: {row5[5]}/-
	Room Type: {row5[6].replace('_', ' ')}       Rooms available: {row5[7]}        Price of the room: {row5[8]}/-
	Room Type: {row5[9].replace('_', ' ')}       Rooms available: {row5[10]}       Price of the room: {row5[11]}/-
	"""
							print(final_item3)
						except IndexError:
							print(f'\nNo information about the hotel: {hotel_name}')
					elif choice2 == 'no':
						pass
					else:
						print('\nEnter a valid command')
				elif choice == 'no':
					pass
				else:
					print('\nEnter a valid command.')
				choice3 = input('\nDo you want to continue to book hotel? ').strip().lower()
				if choice3 == 'yes':
					hotel_name = input('\nEnter hotel\'s name: ').title().strip().replace(' ', '_')
					try:
						pincode5 = int(input('Enter pincode of the hotel: '))
						if int(query_rooms_available(connection_hotel_details, hotel_name)) > 0:
							customer_name = input('Enter your name: ').title().strip().replace(' ','_')
							age = int(input('Enter age: '))
							contact_no = int(input("Enter Contact No.: "))
							email_id = input("Enter Email ID: ")
							room_type = input("Enter type of room you want: ").title().strip().replace(' ','_')
							booked_from = input("Booking From(MM/DD/YY): ").strip()
							booked_to = input("Booking To (MM/DD/YY): ").strip()
							aadhar_no = int(input("Enter Aadhar No.: "))
							time_now = time.strftime('%D')
							aadhar_no_str = len(str(aadhar_no))
							contact_no_str = len(str(contact_no))
							try:
								if aadhar_no_str == 12:
									if contact_no_str == 10:
										amount = amount_payable(connection_hotel_details, hotel_name, pincode5, room_type)
										print('Amount payable is: ', amount, '\n')
										print(display_item4)
										choice4 = input('What do you want to do? ')
										if choice4 == '1':
											print()
											card_no = int(input('Enter no. of your card: '))
											exp = input('Enter expiry(MM/YY): ').strip()
											card_holder_name = input('Enter card holder\'s name: ').strip().upper().replace(' ', '_')
											cvv = int(input('Enter card\'s CVV: '))
											if authenticate_card(card_no_obj=card_no, exp_obj=exp, card_holder_name_obj=card_holder_name, cvv_obj=cvv):
												book_hotel()
											else:
												print('\nPayment Failed')
												continue
										elif choice4 == '2':
											print('\nBooking not initiated')
											print('Exited the booking page')
											continue
										else:
											print('Enter a valid command')
											continue
									else:
										print('\nContact no. is not of 10 digits')
								else:
									print('\nAadhar Card no. is not of 12 digits')
							except IndexError:
								print('\nNo hotel added or no information about it')
								continue
						else:
							print()
							print('Hotel is full!')
					except ValueError:
						print('\nEnter an integer')
				else:
					continue
			elif user_choice == '2':
				row3 = query_view_hotel(connection_hotel_details)
				try:
					row3[0][0]
					for raw_item in row3:
						final_item3 = f"""
		Hotel name: {raw_item[0].replace('_', ' ')}               Place: {raw_item[1].replace('_', ' ')}
		Pincode: {raw_item[2]}            Rooms available: {raw_item[3]}     
				"""
						print(final_item3)
				except IndexError:
					print('\nNo hotel added yet')
			elif user_choice == '3':
				hotel_name = input(
					'\nEnter hotel\'s name: ').title().strip().replace(' ', '_')
				pincode6 = int(input('Enter pincode of the hotel: '))

				try:
					row5 = query_hotel_price(connection_obj=connection_hotel_details,
									  hotel_name_obj=hotel_name,
									  pin_code_obj=pincode6)[0]
					row5[0]
					final_item3 = f"""
		Room Type: {row5[0].replace('_', ' ')}       Rooms available: {row5[1]}        Price of the room: {row5[2]}/-
		Room Type: {row5[3].replace('_', ' ')}       Rooms available: {row5[4]}        Price of the room: {row5[5]}/-
		Room Type: {row5[6].replace('_', ' ')}       Rooms available: {row5[7]}        Price of the room: {row5[8]}/-
		Room Type: {row5[9].replace('_', ' ')}       Rooms available: {row5[10]}       Price of the room: {row5[11]}/-
						"""
					print(final_item3)
				except IndexError:
					print('\nNo information about the hotel')
			elif user_choice == '4':
				customer_name = input(
					'\nEnter your name: ').title().strip().replace(' ', '_')
				aadhar_no = int(input("Enter Aadhar No.: "))
				receipt = generate_ticket_by_query(connection_user_details, connection_obj1=connection_hotel_details,aadhar_obj=aadhar_no, name_obj=customer_name)
				print(receipt)
			elif user_choice == '5':
				user_name = input('\nEnter your name: ').strip().title().replace(' ', '_')
				hotel_name = input('Enter name of the hotel: ').strip().title().replace(' ', '_')
				pincode7 = int(input('Enter pincode of the hotel: '))
				delete_booking(connection_obj=connection_user_details, name_obj=user_name, hotel_name_obj=hotel_name, pincode_obj=pincode7,
							   connection_obj2=connection_hotel_details)
				print('\nBooking cancelled successfully')
			elif user_choice == '6':
				print("""
Exited User Portal successfully""")
				break
			else:
				print('''
Enter a valid command''')
	elif initial_choice == '3':
		exit('''
Good Bye!''')
	else:
		print('''
Enter a valid command''')