from random import randint
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
#import logging
  
async def rps(update: Update, context: CallbackContext):
    user =  update.effective_user.full_name
    #logging.info("%s is playing RPS", user)
    query = update.callback_query
    #replies the query
    await query.answer()
    #create a list of play options
    t = ["Rock", "Paper", "Scissors"]
    #assign a random play to the computer
    computer = t[randint(0,2)]
    #receives the player choice
    playerChoice = query.data
    #edits the inline keyboard to the player choice
    await query.edit_message_text(text="You choose: " + query.data)
    #displays the computer choice
    await query.message.reply_text("I choose " + computer +"!")
    #defines the winner and prints result
    if  playerChoice == computer:
        await query.message.reply_text("Tie!")
    elif playerChoice == "Rock":
        if computer == "Paper":
            await query.message.reply_text(f"You lose! {computer} covers {playerChoice}")
        else:
            await query.message.reply_text(f"You win! {playerChoice} smashes {computer}")
    elif playerChoice == "Paper":
        if computer == "Scissors":
            await query.message.reply_text(f"You lose! {computer} cut {playerChoice}")
        else:
            await query.message.reply_text(f"You win! {playerChoice} covers {computer}")
    elif playerChoice == "Scissors":
        if computer == "Rock":
            await query.message.reply_text(f"You lose! {computer} smashes {playerChoice}")
        else:
            await query.message.reply_text(f"You win! {playerChoice} cut {computer}")

        
async def rpsStart(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Rock", callback_data='Rock'),
                 InlineKeyboardButton("Paper", callback_data='Paper')],

                [InlineKeyboardButton("Scissors", callback_data='Scissors')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Sure, lets play Rock Paper and Scissors!', reply_markup=reply_markup)