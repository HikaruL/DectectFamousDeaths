from __future__ import print_function
import twitter

ACCESS_TOKEN = '93130558-dO7HqvIOEr3K3m5fJV087VZ73RN0gaEaYkUWgWe4Y'
ACCESS_SECRET = 'Ro0zxJPCOJExF6Vyy80NypFhanpA9twEvhUIzkS6OwmsU'
CONSUMER_KEY = 'N3XWvJDOcOt7eUqteJpLySANQ'
CONSUMER_SECRET = 'Jpi0Q2fIqA06CKzz0BFwRd77QOSE6u8WHjOrR03coZvwO3RVEj'


# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_SECRET)


statuses = api.GetSearch(term="the", lang="en")
current_max = 0
for status in statuses:
    current_max = max(current_max, status.id)
    print(status.text)

statuses = api.GetSearch(term="on", lang="en", max_id=current_max)
for status in statuses:
    current_max = max(current_max, status.id)
    print(status.text)

