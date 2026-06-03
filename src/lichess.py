import berserk
import chess

#TOKEN = ""

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)

client.opening_explorer