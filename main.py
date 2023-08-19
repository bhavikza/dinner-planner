import os
import random
import telebot

# Replace with your actual bot token
token = os.environ['YOUR_BOT_TOKEN']
# Replace with your actual chat ID
chatid = os.environ['CHAT_ID']

bot = telebot.TeleBot(token)

# List to store meal names
meal_names = []

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Dinner Planner Bot! You can add, rename, delete, delete all, view meal names, and request a weekly plan.")

@bot.message_handler(commands=['add'])
def add_meal(message):
    meals = message.text[5:]  # Extract the meal names from the command
    if meals:
        new_meals = meals.split(",")
        new_meals = [meal.strip() for meal in new_meals]  # Remove leading/trailing spaces
        # Check for duplicate meal names
        unique_new_meals = [meal for meal in new_meals if meal not in meal_names]
        meal_names.extend(unique_new_meals)
        added_count = len(unique_new_meals)
        if added_count == 0:
            bot.reply_to(message, "No new meal names added (all duplicates).")
        else:
            bot.reply_to(message, f"Added {added_count} unique meal(s) to the meal list.")
    else:
        bot.reply_to(message, "Please provide meal name(s) to add.")

@bot.message_handler(commands=['rename'])
def rename_meal(message):
    parts = message.text.split()
    if len(parts) != 3:
        bot.reply_to(message, "Usage: /rename <meal_number> <new_name>")
        return
    
    meal_number = int(parts[1]) - 1  # Adjust to 0-based index
    new_name = parts[2]
    
    if 0 <= meal_number < len(meal_names):
        old_name = meal_names[meal_number]
        if new_name not in meal_names:
            meal_names[meal_number] = new_name
            bot.reply_to(message, f"Renamed '{old_name}' to '{new_name}'.")
        else:
            bot.reply_to(message, f"'{new_name}' is already in the meal list.")
    else:
        bot.reply_to(message, f"Invalid meal number.")

@bot.message_handler(commands=['delete'])
def delete_meal(message):
    if not meal_names:
        bot.reply_to(message, "The meal list is empty.")
        return

    meal_list_text = "\n".join([f"{i+1}. {meal}" for i, meal in enumerate(meal_names)])
    bot.reply_to(message, f"List of Meal Names:\n{meal_list_text}\n\nPlease specify the number of the meal you want to delete using /delete <meal_number>.")

@bot.message_handler(commands=['deleteconfirm'])
def confirm_delete(message):
    meal_number = int(message.text.split()[1]) - 1  # Adjust to 0-based index

    if 0 <= meal_number < len(meal_names):
        deleted_meal = meal_names.pop(meal_number)
        bot.reply_to(message, f"Deleted meal: {deleted_meal}")
    else:
        bot.reply_to(message, f"Invalid meal number.")

@bot.message_handler(commands=['list'])
def list_meals(message):
    if meal_names:
        meals_text = "\n".join([f"{i+1}. {meal}" for i, meal in enumerate(meal_names)])
        bot.reply_to(message, f"List of Meal Names:\n{meals_text}")
    else:
        bot.reply_to(message, "The meal list is empty.")

@bot.message_handler(commands=['plan'])
def generate_plan(message):
    if len(meal_names) >= 5:
        weekly_plan = random.sample(meal_names, 5)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        plan_text = "Weekly Meal Plan:\n"
        for day, meal in zip(days, weekly_plan):
            plan_text += f"{day}: {meal}\n"
        bot.reply_to(message, plan_text)
    else:
        bot.reply_to(message, "Not enough meal names to generate a plan. Please add at least 5 meal names.")

@bot.message_handler(commands=['deleteall'])
def delete_all_meals(message):
    global meal_names
    meal_names = []
    bot.reply_to(message, "All meal names have been deleted.")

# Run the bot
bot.polling()
