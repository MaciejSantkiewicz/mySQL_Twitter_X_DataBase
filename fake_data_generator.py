import mysql.connector
import random
from datetime import datetime
from faker import Faker


db_config = { #login to your mysql server
    'user': 'xxx',
    'password': 'xxx',
    'host': 'xxx',
    'database': 'xxx'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

fake = Faker()

date_format = "%Y-%m-%d"

def fetch_table_count(table_name: str):
    fetch_table = table_name
    count_query = f"SELECT count(*) from {fetch_table}"
    cursor.execute(count_query)
    result = cursor.fetchone()
    return result[0]


def insert_new_users(number_of_insers: int): #create new users
    inserts = number_of_insers #number of new users to insert
    table_name = 'users' #name of the table
    
    for insert in range(inserts):
        try:
            fake_name = fake.user_name()

            fake_timestamp = str(fake.date()) + " " + str(fake.time())

            insert_query = f"INSERT INTO {table_name} (user_name, created_at) VALUES (%s, %s)"
            
            cursor.execute(insert_query, (fake_name, fake_timestamp))
            conn.commit()
        except Exception as e:
            print(e)



def insert_new_followers(number_of_inserts: int): #set followers
    inserts_to_do = number_of_inserts  #number new follows
    inserts_left = inserts_to_do
    failed_attemps = 0

    table_name = 'followers'#name of the table


    for insert in range(inserts_to_do):
        while inserts_left != 0:
            try:
                id_of_users_1 = random.randrange(fetch_table_count("users"))
                id_of_users_2 = random.randrange(fetch_table_count("users"))
                fake_date = fake.date()
                fake_time = fake.time()
                fake_timestamp = str(fake_date) + " " + str(fake_time)

                get_first_user = f"select date(created_at) from users where id = {id_of_users_1}"
                cursor.execute(get_first_user)
                user_reg_date = datetime.strptime(str(cursor.fetchone()[0]), date_format)

                timestamp_date = datetime.strptime(str(fake_date), date_format)

                date_difference = user_reg_date - timestamp_date                    
                if date_difference.days > 0: #cheks if the timestamp of the follow didn't occure before the user registration
                    pass  
                else:
                    insert_query = f"INSERT INTO {table_name} (follower_id, followee_id, created_at) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (id_of_users_1, id_of_users_2,  fake_timestamp))
                    conn.commit()
                    inserts_left -= 1

            except Exception as e:
                failed_attemps += 1
        else:
            pass
    else:
        print("INSERT NEW FOLLOWS: Task Completed. " + f"Failed Attempts= {failed_attemps/inserts_to_do}%") 
          


def insert_new_likes(number_of_inserts: int): #set followers

    inserts_to_do = number_of_inserts  #number new follows
    inserts_left = inserts_to_do
    failed_attemps = 0

    table_name = 'likes'#name of the table


    for insert in range(inserts_to_do):
        while inserts_left != 0:
            try:
                user_id = random.randrange(fetch_table_count("users"))
                tweet_id = random.randrange(fetch_table_count("tweets"))
                fake_date = fake.date()
                fake_time = fake.time()
                fake_timestamp = str(fake_date) + " " + str(fake_time)

                get_first_user = f"select date(created_at) from users where id = {user_id}"
                cursor.execute(get_first_user)
                user_reg_date = datetime.strptime(str(cursor.fetchone()[0]), date_format)

                timestamp_date = datetime.strptime(str(fake_date), date_format)

                date_difference = user_reg_date - timestamp_date 
                if date_difference.days < 0:
                    pass
                else:
                    insert_query = f"INSERT INTO {table_name} (user_id, tweet_id, created_at) VALUES (%s, %s, %s)" 
                    cursor.execute(insert_query, (user_id, tweet_id,  fake_timestamp))
                    conn.commit()
                    inserts_left -= 1

            except Exception as e:
                failed_attemps += 1
        else:
            pass
    else:
        print("INSERT NEW LIKES: Task Completed. " + f"Failed Attempts= {failed_attemps/inserts_to_do}%")


def insert_new_tweet(number_of_inserts: int):
    inserts_to_do = number_of_inserts  #number new follows
    inserts_left = inserts_to_do

    table_name = 'tweets' #name of the table

    for insert in range(inserts_to_do):
        while inserts_left != 0:
            try:
                id_of_users = random.randrange(fetch_table_count("users"))

                fake_tweet = fake.paragraph(random.randrange(1,3))
                fake_date = fake.date()
                fake_time = fake.time()
                fake_timestamp = str(fake_date) + " " + str(fake_time)

                get_user = f"select date(created_at) from users where id = {id_of_users}"
                cursor.execute(get_user)
                user_reg_date = datetime.strptime(str(cursor.fetchone()[0]), date_format)

                timestamp_date = datetime.strptime(str(fake_date), date_format)

                date_difference = user_reg_date - timestamp_date 
                if date_difference.days < 0:
                    pass
                else:
                    insert_query = f"INSERT INTO {table_name} (tweet_text, created_at, user_id) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (fake_tweet, fake_timestamp, id_of_users))
                    conn.commit()
                    inserts_left -= 1

            except Exception as e:
                print(e)
        else:
            pass
    else:
        print("INSERT NEW TWEETS: Task Completed")




def create_new_data(
        number_of_new_users: int, 
        number_of_new_tweets: int, 
        number_of_new_likes: int, 
        number_of_new_follows: int ):
    
    insert_new_users(number_of_new_users)
    insert_new_tweet(number_of_new_tweets)
    insert_new_likes(number_of_new_likes)
    insert_new_followers(number_of_new_follows)



cursor.close()
conn.close()
