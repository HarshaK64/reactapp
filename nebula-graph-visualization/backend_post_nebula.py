import pandas as pd
from nebula2.Client import GraphClient

# Load your DataFrame from the 'emails.csv' file
nRowsRead = 1000
df1 = pd.read_csv('emails.csv', delimiter=',', nrows=nRowsRead)

# Extract sender and recipients from the 'message' column
df1['sender'] = df1['message'].str.extract(r'From: (.+?)(?=\r\n)')[0]
df1['recipients'] = df1['message'].str.extract(r'To: (.+?)(?=\r\n)')[0]

# Create a new DataFrame to represent relationships
relationships = df1[['sender', 'recipients']].dropna()

# Initialize a Nebula Graph client and connect to the server
client = GraphClient('your_nebula_server_ip', 9669)

# Authenticate with username and password if required
# client.authenticate('username', 'password')

# Establish a connection
client.connect()

# Insert data into Nebula Graph
for index, row in relationships.iterrows():
    sender = row['sender']
    recipient = row['recipients']

    # Insert sender and recipient as vertices
    query = f'INSERT VERTEX person(name) VALUES "{sender}":("{sender}"), "{recipient}":("{recipient}")'
    client.execute(query)

    # Insert an edge representing the relationship
    query = f'INSERT EDGE email_sent(sender) VALUES "{sender}":("{sender}") -> "{recipient}":("{recipient}")'
    client.execute(query)

# Close the connection
client.signout()
client.disconnect()
