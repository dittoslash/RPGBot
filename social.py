import asyncio
import discord
import formatting
import core
from core import Parsing
from core import Tokens
from files import User
from files import Item


def new_user(author):
    new = User(author, author.id)
    return new


async def character_creation(par, msg, player):
    # stage 0: initial message
    # stage 1: initial message sent, waiting for class chosen
    # ...
    cha = msg.channel
    stage = player.status[1]
    classes = Parsing.classes

    if stage == 0:
        classes_desc = [(value, key['description']) for value, key in classes.items()]
        print(classes_desc)
        embed = formatting.enum_choices(classes_desc)
        await cha.send(embed=embed)
        player.status[1] = 1
        player.save_self()
        await asyncio.sleep(60)
        try:
            if player.status[0] == 'creator' and player.status[1] == 1:
                await cha.send('timed out')
                player.remove_self()
        except IndexError:
            await cha.send('timed out')
            player.remove_self()

        return

    if stage == 1:
        for i in range(len(par)):
            try:
                par[i] = int(par[i])
            except:
                return
        if par[0] > 0 and par[0] <= len(classes):
            chosen = par[0] - 1
            chosen = list(classes.keys())[chosen]
            await cha.send('You chose {}'.format(chosen))
            player.status = ['None']
            await player.give_starter(chosen)
            await player.give_item('gold', 100)
            player.save_self()
            await asyncio.sleep(3)
            await cha.send('Character succesfully created!')
        else:
            await msg.channel.send('Invalid choice')

        return
