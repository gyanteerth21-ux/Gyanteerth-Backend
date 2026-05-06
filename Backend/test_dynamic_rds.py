import boto3
import psycopg2

try:
    print("Attempting to generate RDS auth token...")
    client = boto3.client('rds', region_name='us-east-1')
    auth_token = client.generate_db_auth_token(
        DBHostname='database-1.cluster-csx8cqgegpow.us-east-1.rds.amazonaws.com',
        Port=5432,
        DBUsername='postgres',
        Region='us-east-1'
    )
    print("Token generated successfully!")
    
    conn = psycopg2.connect(
        host='database-1.cluster-csx8cqgegpow.us-east-1.rds.amazonaws.com',
        port=5432,
        database='postgres',
        user='postgres',
        password=auth_token,
        sslmode='require'
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('SELECT version();')
    print("Connection successful with dynamic token!")
    print(cur.fetchone()[0])
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
