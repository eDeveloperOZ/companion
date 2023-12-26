import csv
import re
import sys
import tty
import termios

def read_messages(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        messages = re.split(r'\n\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{2}:\d{2} - -\d+:\s', content)
        return messages[1:]

def get_single_key_press():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def process_messages(messages, output_file):
    try:
        with open(output_file, 'a', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for message in messages:
                print("\nMessage:", message.strip())
                print("Press 1 (send) or 0 (don't send): ", end='', flush=True)
                user_input = get_single_key_press()
                while user_input not in ['0', '1']:
                    print("\nInvalid input. Press 1 (send) or 0 (don't send): ", end='', flush=True)
                    user_input = get_single_key_press()
                writer.writerow([message.strip(), user_input])
    except KeyboardInterrupt:
        print("\nProcess interrupted. Your progress has been saved.")
    except Exception as e:
        print(f"An error occurred: {e}")

input_file = 'channel_messages.txt'  # Replace with your file path
output_file = 'processed_messages.csv'  # The file where the processed data will be stored

messages = read_messages(input_file)
process_messages(messages, output_file)
