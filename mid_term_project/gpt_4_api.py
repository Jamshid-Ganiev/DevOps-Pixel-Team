from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("GPT_4_API_KEY"))

def ask_question():
    question = input("What do you want to know?\nEnter your question: ")
    return question

def get_answer(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer the user's questions professionally."},
                {"role": "user", "content": prompt}
            ]
        )
        response = completion
        if response.choices:
            return response.choices[0].message.content
        else:
            return "Sorry, I couldn't understand your question."
    except Exception as e:
        # handles exceptions, like API errors
        return f"An error occurred: {str(e)}"

def get_city_info(city_name):
    try:
        prompt = f"What are the best time to travel to {city_name}?,"\
                 f" available airlines to {city_name}, famous foods in {city_name},"\
                 f" tourist attractions in {city_name}, and population of {city_name}?"\
                 f" give the answer in bullet points."
        
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant. Answer the questions professionally and make your asnwers as compact as possbile by keeping the core meaning."},
                {"role": "user", "content": prompt}
            ]
        )

        response = completion
        if response.choices:
            return response.choices[0].message.content
        else:
            return "Sorry, I couldn't understand your question."
    except Exception as e:
        return f"An error occurred while fetching city information: {str(e)}"

def main():
    while True:
        print("Choose an option:")
        print("1. City Information")
        print("2. Chat with ChatGPT")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            city_name = input("Enter the city name or country name: ")
            city_info = get_city_info(city_name)
            print(city_info)
        elif choice == "2":
            while True:
                question = ask_question()
                choices = ["no", "n", "exit", "quit", "bye"]
                if question.lower() in choices:
                    break
                answer = get_answer(question)
                print(answer)
                print("\n")
        else:
            print("Invalid choice. Please enter either 1 or 2.")

        user_input = input("Do you want to continue? (yes/no): ")
        if user_input.lower() not in ["yes", "y"]:
            break

if __name__ == "__main__":
    main()
