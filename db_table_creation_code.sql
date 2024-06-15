create database twitter_x;
use twitter_x;

create table users(
	id int auto_increment primary key, 
    user_name varchar(255) unique not null,
    create_at timestamp	default now()
    );

create table tweets(
	id int auto_increment primary key, 
    tweet_text varchar(255) not null,
    create_at timestamp	default now(),
    user_id int not null,
    
    foreign key(user_id) references users(id)
    );
    
create table likes(
	user_id int not null,
    tweet_id int not null,
    created_at timestamp default now(),
    
    foreign key(user_id) references users(id),
    foreign key(tweet_id) references tweets(id),
    primary key(user_id, tweet_id)
    );
    
create table followers(
	follower_id int not null,
    followee_id int not null,
    
    foreign key(follower_id) references users(id),
    foreign key(followee_id) references users(id),
    primary key(follower_id, followee_id)
	);
    
	
