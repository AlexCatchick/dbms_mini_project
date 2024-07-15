import mysql.connector
from mysql.connector import Error

def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="mV3m@json"
        )
        print("Connection to MySQL server successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def create_database(connection):
    if connection is None:
        print("No connection to MySQL server.")
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS NMIT_Sports_Hub")
        print("Database 'NMIT_Sports_Hub' created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",     # Replace with your MySQL username
            passwd="your_password",   # Replace with your MySQL password
            database="NMIT_Sports_Hub"
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def execute_query(connection, query):
    if connection is None:
        print("No connection to MySQL DB.")
        return
    
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def create_tables(connection):
    create_players_table = """
    CREATE TABLE IF NOT EXISTS Players (
        player_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT NOT NULL,
        sport VARCHAR(255) NOT NULL
    );
    """

    create_teams_table = """
    CREATE TABLE IF NOT EXISTS Teams (
        team_id INT AUTO_INCREMENT PRIMARY KEY,
        team_name VARCHAR(255) NOT NULL,
        sport VARCHAR(255) NOT NULL
    );
    """

    create_team_players_table = """
    CREATE TABLE IF NOT EXISTS Team_Players (
        team_id INT,
        player_id INT,
        FOREIGN KEY (team_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
        FOREIGN KEY (player_id) REFERENCES Players(player_id) ON DELETE CASCADE
    );
    """

    create_matches_table = """
    CREATE TABLE IF NOT EXISTS Matches (
        match_id INT AUTO_INCREMENT PRIMARY KEY,
        team1_id INT,
        team2_id INT,
        team1_score INT,
        team2_score INT,
        match_date DATE,
        FOREIGN KEY (team1_id) REFERENCES Teams(team_id) ON DELETE CASCADE,
        FOREIGN KEY (team2_id) REFERENCES Teams(team_id) ON DELETE CASCADE
    );
    """

    execute_query(connection, create_players_table)
    execute_query(connection, create_teams_table)
    execute_query(connection, create_team_players_table)
    execute_query(connection, create_matches_table)

def add_player(connection):
    name = input("Enter player name: ")
    age = int(input("Enter player age: "))
    sport = input("Enter sport: ")
    query = f"INSERT INTO Players (name, age, sport) VALUES ('{name}', {age}, '{sport}')"
    execute_query(connection, query)

def delete_player(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Players")
    count = cursor.fetchone()[0]

    if count == 0:
        print("No players to delete.")
        return
    
    player_id = int(input("Enter player ID to delete: "))
    delete_player_query = f"DELETE FROM Players WHERE player_id = {player_id}"
    execute_query(connection, delete_player_query)
    
    delete_team_players_query = f"DELETE FROM Team_Players WHERE player_id = {player_id}"
    execute_query(connection, delete_team_players_query)
    
    print(f"Player with ID {player_id} deleted successfully.")

def create_team(connection):
    team_name = input("Enter team name: ")
    sport = input("Enter sport: ")
    query = f"INSERT INTO Teams (team_name, sport) VALUES ('{team_name}', '{sport}')"
    execute_query(connection, query)

def delete_team(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Teams")
    count = cursor.fetchone()[0]

    if count == 0:
        print("No teams to delete.")
        return
    
    team_id = int(input("Enter team ID to delete: "))
    delete_team_query = f"DELETE FROM Teams WHERE team_id = {team_id}"
    execute_query(connection, delete_team_query)
    
    delete_team_players_query = f"DELETE FROM Team_Players WHERE team_id = {team_id}"
    execute_query(connection, delete_team_players_query)
    
    delete_matches_query = f"DELETE FROM Matches WHERE team1_id = {team_id} OR team2_id = {team_id}"
    execute_query(connection, delete_matches_query)
    
    print(f"Team with ID {team_id} deleted successfully.")

def assign_player_to_team(connection):
    team_id = int(input("Enter team ID: "))
    player_id = int(input("Enter player ID: "))
    query = f"INSERT INTO Team_Players (team_id, player_id) VALUES ({team_id}, {player_id})"
    execute_query(connection, query)

def record_match_result(connection):
    team1_id = int(input("Enter Team 1 ID: "))
    team2_id = int(input("Enter Team 2 ID: "))
    team1_score = int(input("Enter Team 1 score: "))
    team2_score = int(input("Enter Team 2 score: "))
    match_date = input("Enter match date (YYYY-MM-DD): ")
    query = f"""
    INSERT INTO Matches (team1_id, team2_id, team1_score, team2_score, match_date) 
    VALUES ({team1_id}, {team2_id}, {team1_score}, {team2_score}, '{match_date}')
    """
    execute_query(connection, query)

def display_teams_and_players(connection):
    query = """
    SELECT t.team_name, p.name 
    FROM Teams t 
    LEFT JOIN Team_Players tp ON t.team_id = tp.team_id 
    LEFT JOIN Players p ON tp.player_id = p.player_id
    """
    result = fetch_query(connection, query)
    if result:
        for row in result:
            team_name = row[0]
            player_name = row[1] if row[1] else "No players assigned"
            print(f"Team: {team_name}, Player: {player_name}")

def display_match_results(connection):
    query = """
    SELECT m.match_id, t1.team_name AS team1, t2.team_name AS team2, m.team1_score, m.team2_score, m.match_date 
    FROM Matches m 
    JOIN Teams t1 ON m.team1_id = t1.team_id 
    JOIN Teams t2 ON m.team2_id = t2.team_id
    """
    result = fetch_query(connection, query)
    if result:
        for row in result:
            match_id = row[0]
            team1_name = row[1]
            team2_name = row[2]
            team1_score = row[3]
            team2_score = row[4]
            match_date = row[5]
            print(f"Match ID: {match_id}, {team1_name} vs {team2_name}, Score: {team1_score}-{team2_score}, Date: {match_date}")

def fetch_query(connection, query):
    if connection is None:
        print("No connection to MySQL DB.")
        return None
    
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def main():
    server_connection = create_server_connection()
    create_database(server_connection)

    connection = create_connection()
    if connection:
        create_tables(connection)

        while True:
            print("\nNMIT Sports Hub Menu:")
            print("1. Add new player")
            print("2. Delete a player")
            print("3. Create team")
            print("4. Delete a team")
            print("5. Assign player to team")
            print("6. Record match result")
            print("7. Display teams and their players")
            print("8. Display match results")
            print("9. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                add_player(connection)
            elif choice == '2':
                delete_player(connection)
            elif choice == '3':
                create_team(connection)
            elif choice == '4':
                delete_team(connection)
            elif choice == '5':
                assign_player_to_team(connection)
            elif choice == '6':
                record_match_result(connection)
            elif choice == '7':
                display_teams_and_players(connection)
            elif choice == '8':
                display_match_results(connection)
            elif choice == '9':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
