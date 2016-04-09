#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

class DB:

    def __init__(self, db_conn ="dbname=tournament"):
        '''
        Initiates DB connection via defoult value (string) if no parameter
        '''        
        self.conn = psycopg2.connect(db_conn)
    
    def cursor(self):
        '''
        Returns cursor
        '''
        return self.conn.cursor()

    def execute(self, sql_query, parametr=None, close_connection=False):
        '''
        Executes SQL queries, commits and closes connection if necessary
        '''

        cursor = self.cursor()
        if type(parametr) == tuple:
            cursor.execute(sql_query, parametr)
        else:
            cursor.execute(sql_query)
        if close_connection:
            self.conn.commit()
            self.close()
        return {"conn": self.conn, "cursor": cursor if not close_connection else None}

    def close(self):
        '''
        Closes DB connection
        '''
        return self.conn.close()


def deleteMatches():
    """Remove all the match records FROM the database."""
    DB().execute("DELETE FROM matches", None, True)

def deletePlayers():
    """Remove all the player records FROM the database."""
    DB().execute("DELETE FROM players", None, True)

def countPlayers():
    """Returns the number of players currently registered."""
    conn = DB().execute("SELECT count(*) AS num_players FROM players;")
    data = conn["cursor"].fetchone()
    conn['conn'].close()
    return data[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players (name) VALUES (%s);"
    parametr = (name,)
    conn = DB().execute(query, parametr, True)

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = DB().execute("SELECT * from num_matches;", None, False)
    data = conn["cursor"].fetchall()
    conn['conn'].close()
    return data

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    parametr = (winner, loser,)
    conn = DB().execute(query, parametr, True)
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ranking = playerStandings()
    print ranking
    if len(ranking) % 2 == 0:
        result = []
        for i in range(0, len(ranking), 2):
            result.append((ranking[i][0],ranking[i][1], ranking[i+1][0],ranking[i+1][1]))
        return result
    else:
        print "Number of players is odd!"

