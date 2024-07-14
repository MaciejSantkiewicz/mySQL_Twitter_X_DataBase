-- Top 10 accounts with biggest following--
select user_name, count(follower_id) as number_of_followers from followers 
	join users on users.id = follower_id
group by follower_id 
order by number_of_followers desc
limit 10;

-- Top 10 accounts with most tweets--
select user_name, count(tweet_text) as number_of_tweets from users
	join tweets on users.id = tweets.user_id
group by user_name
order by number_of_tweets desc
limit 10;