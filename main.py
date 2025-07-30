
import base64
import os
import logging
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename='user_feedback.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

console = Console()

def collect_feedback():
    print("We'd love your feedback! Type your thoughts below:")
    feedback = input(">>> ")

    if feedback.strip():
        logging.info(f'User Feedback: {feedback}')
        print("✅ Feedback received and logged.")
    else:
        print("⚠️ No feedback provided.")


def generate(prompt):
    print("\n\n***************\nYour prompt:\n" + prompt + "\n")
    print("AI Response: \n")
    client = genai.Client(
        api_key=os.getenv("API_KEY")
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
    )
    txt=''
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        console.print(Markdown(chunk.text), end="")

def summarize():
    console.print(Markdown("""
Select a prompt:
1. Generate high-level summary.
2. Keypoints: Extract discrete main ideas or takeaways.
3. Professional and detailed summary.
          """))
    choice=int(input("Enter your choice: "))
    if choice==1:
        article=input("Enter document/article to summarize: \n")
        generate("Summarize the following post: " + article)
    elif choice==2:
        article=input("Enter paragraph to extract keypoints: \n")
        generate("Hey, I don’t have time to read all this. What are the main points of this text: " + article)
    elif choice==3:
        article=input("Enter text to generate professional summary: \n")
        generate("Please analyze this report and provide a structured summary with key findings, recommendations, and conclusions:  " + article)
    else:
        print("Please enter valid choice.")

def advice():
    console.print(Markdown("""
Select a prompt:
1. Time management habits
2. Encouragement and mindset coaching.
3. Handling burn-outs.
          """))
    choice=int(input("Enter your choice: "))
    if choice==1:
        generate("How can I build better time management habits?")
    elif choice==2:
        generate("I’ve lost confidence lately. What’s your advice to help me regain it?")
    elif choice==3:
        generate("I feel burnt out at work, and it’s affecting my mood. Any advice on how to recharge emotionally?")
    else:
        print("Please enter valid choice")

def improve():
    console.print(Markdown("""
Select a prompt:
1. Grammar and style enhancement
2. Email Tone transformation
3. Creative rework for social media
          """))
    choice=int(input("Enter your choice: "))
    if choice==1:
        article=input("Enter email/article: \n")
        generate("Edit the following paragraph for clarity and grammatical correctness: " + article)
    elif choice==2:
        article=input("Enter email: \n")
        generate("Rewrite this email to sound warm and professional:  " + article)
    elif choice==3:
        article=input("Enter post to rewrite: \n")
        generate("Rewrite this post to be more engaging and appealing for social media audiences:  " + article)
    else:
        print("Please enter valid choice.")

def planning():
    console.print(Markdown("""
Select a prompt:
1. 3-month competitive exam study plan
2. Instagram content calendar
3. 30 day project sprint
          """))
    choice=int(input("Enter your choice: "))
    if choice==1:
        generate("Design a study plan to prepare for competitive exams in 3 months.")
    elif choice==2:
        generate("Design a content calendar for a small business on Instagram, with post ideas and timing for one month.")
    elif choice==3:
        generate("Generate a 30 day sprint for a SaaS project.")
    else:
        print("Please enter valid choice")

def translate():
    console.print(Markdown("""
Select a prompt:
1. Translate English to Spanish.
2. Rewrite documentation for casual users
3. Change writing tone for business/formal purposes.

          """))
    choice=int(input("Enter your choice: "))
    if choice==1:
        article=input("Enter English article to translate: \n")
        generate("Translate this post from English to Spanish: " + article)
    elif choice==2:
        article=input("Enter software documentation: \n")
        generate("Rewrite this software documentation for someone with no technical background: " + article)
    elif choice==3:
        article=input("Enter text to rewrite: \n")
        generate("Make this casual note sound more persuasive and formal for a business proposal: " + article)
    else:
        print("Please enter valid choice.")

def start():
    while True:
        console.print(Markdown("""
# PromptNest

Menu:
1. Summarize, extract and understand text
2. Personal advice
3. Improve and rewrite emails/articles.
4. Planning and Organizing
5. Translating and shift tones
6. Exit

Enter your choice.
              """), style="")
        choice=int(input())
        if choice==1:
            summarize()
        elif choice==2:
            advice()
        elif choice==3:
            improve()
        elif choice==4:
            planning()
        elif choice==5:
            translate()
        elif choice==6:
            collect_feedback()
            print("Exiting...")
            return
        else:
            print("Enter valid choice between 1-6")

if __name__ == "__main__":
    start()