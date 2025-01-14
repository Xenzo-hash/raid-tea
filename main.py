import os
import shutil
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
import tkinter as tk
from tkinter import messagebox, Toplevel

webhook_url = ""
message = ""
delay = 0.5
amount = 1

def gradient_color(text, start_rgb=(0, 0, 128), end_rgb=(255, 255, 255), ratio=0):
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
    return "".join(f"\033[38;2;{r};{g};{b}m{char}" for char in text)

def display_text_with_gradient(lines, padding=0, start_rgb=(0, 0, 128), end_rgb=(255, 255, 255)):
    total_lines = len(lines)
    for i, line in enumerate(lines):
        ratio = i / max(total_lines - 1, 1)
        print(" " * padding + gradient_color(line, start_rgb, end_rgb, ratio))

def display_banner():
    banner_lines = [
        "  /$$                              ",
        " | $$                              ",
        " /$$$$$$  /$$   /$$| $$  /$$$$$$$  /$$$$$$   /$$$$$$ ",
        "/$$__  $$| $$  | $$| $$ /$$_____/ |____  $$ /$$__  $$",
        "| $$  \\ $$| $$  | $$| $$|  $$$$$$   /$$$$$$$| $$  \\__/",
        "| $$  | $$| $$  | $$| $$ \\____  $$ /$$__  $$| $$      ",
        "| $$$$$$$/|  $$$$$$/| $$ /$$$$$$$/|  $$$$$$$| $$      ",
        "| $$____/  \\______/ |__/|_______/  \\_______/|__/      ",
        "| $$                                                  ",
        "| $$                                                  ",
        "|__/                                                  "
    ]

    terminal_size = shutil.get_terminal_size((80, 24))
    padding = max((terminal_size.columns - len(max(banner_lines, key=len))) // 2, 0)
    display_text_with_gradient(banner_lines, padding=padding)
    pulsar_text = ["pulsar 1.0.0"]
    display_text_with_gradient(pulsar_text, padding=(terminal_size.columns - len(pulsar_text[0])) // 2)

def send_messages(driver, message, num_messages):
    time.sleep(5)
    message_box = driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")
    for i in range(num_messages):
        message_box.send_keys(message)
        message_box.send_keys(Keys.RETURN)
        if i % 5 == 0:
            print("Taking a short break to avoid rate limits...")
            time.sleep(5)
        else:
            time.sleep(0.1)
    print("Finished sending messages!")
    driver.quit()

def run_spammer(message, num_messages, account_number):
    edge_options = Options()
    edge_options.use_chromium = True
    driver = webdriver.Edge(options=edge_options)
    driver.get("https://discord.com/login")
    input(f"Press Enter in tab {account_number + 1} after logging in and selecting the channel...")
    send_messages(driver, message, num_messages)

def display_webhook_menu():
    print("\n[01] Set webhook-link")
    print("[02] Set message")
    print("[03] Set message-delay (in seconds)")
    print("[04] Set message-amount")
    print("[05] Start Spamming")
    print("[06] Exit to main menu")

def main():
    global webhook_url, message, delay, amount
    while True:
        display_banner()
        print("\n[01] webhook-spam")
        choice = input("\nEnter an option: ").strip()
        if choice == "01":
            while True:
                display_webhook_menu()
                sub_choice = input("\nChoose an action: ").strip()
                if sub_choice == "01":
                    webhook_url = input("Enter webhook URL: ").strip()
                elif sub_choice == "02":
                    message = input("Enter message to send: ").strip()
                elif sub_choice == "03":
                    delay = float(input("Enter message delay (seconds): ").strip())
                elif sub_choice == "04":
                    amount = int(input("Enter number of messages to send: ").strip())
                elif sub_choice == "05":
                    threading.Thread(target=run_spammer, args=(message, amount, 0)).start()
                elif sub_choice == "06":
                    break
                else:
                    print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
