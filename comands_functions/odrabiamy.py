from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from time import sleep
from PIL import Image
import discord
import os

# Ścieżka do przeglądarki, w której są zapisane dane do logowania do odrabiamy.pl
profile_path = r"C:\Users\mariu\AppData\Local\Google\Chrome\User Data"

# Konfiguracja selenium
options = Options()
options.add_argument("start-maximized")
options.add_argument(f"user-data-dir={profile_path}")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)


# Funkcja asynchroniczna wysyłająca zrzuty ekranu na Discord
async def send_screenshots(interaction: discord.Interaction, files_names, curr_link, exercises_numbers, index):
    if interaction is not None:
        await interaction.channel.send(f"# Zadanie {exercises_numbers[index]}, {curr_link[5].replace('-', ' ')}", silent=True)
        for file in files_names:
            with open(file, 'rb') as f:
                await  interaction.channel.send(file=discord.File(f), silent=True)
            os.remove(file)
    else:
        print('Nie udało się znaleźć kanału.')

# Funkcja do robienia zrzutów ekranu i przygotowania do wysyłki
def make_screenshots(book, page):
    driver.get(f"https://odrabiamy.pl/{book}/strona-{page}")
    driver.maximize_window()
    sleep(2)

    links = []
    exercises_numbers = []
    homework_exercises = driver.find_elements(By.CLASS_NAME, 'Chip_chip__WbCj7')

    for exercise in homework_exercises:
        links.append(exercise.get_attribute("href"))
        number = exercise.get_attribute("id")[-2:]
        exercises_numbers.append(number[-1]) if number[0] == "-" else exercises_numbers.append(number)
            
    # Lista z plikami, które będą wysyłane
    all_files_to_send = []

    for index, link in enumerate(links):
        driver.get(link)
        sleep(2)

        curr_link = link.split("/")

        max_scroll = driver.execute_script("return document.body.scrollHeight")
        curr_scroll = 0
        screenshot_count = 0
        files_names = []

        while curr_scroll < max_scroll:
            screenshot_count += 1
            curr_file_name = f"{curr_link[5]}_zadanie-{exercises_numbers[index]}_{screenshot_count}.png"
            img_name = curr_file_name
            driver.save_screenshot(img_name)

            files_names.append(curr_file_name)

            # Przycinanie obrazka
            img = Image.open(img_name)
            width, height = img.size
            left = 200
            right = width - 700
            top = 0
            bottom = height
            cropped_img = img.crop((left, top, right, bottom))
            cropped_img.save(img_name)

            curr_scroll += 620
            
            if max_scroll - curr_scroll < 300:
                break

            driver.execute_script(f"window.scrollTo(0, {curr_scroll});")

        # Dodajemy zrobione pliki do listy do wysyłki
        all_files_to_send.append((files_names, curr_link, exercises_numbers, index))

    return all_files_to_send

# Asynchroniczna funkcja wysyłająca wszystkie zrzuty
async def send_all_screenshots(interaction: discord.Interaction, all_files_to_send):
    for files_names, curr_link, exercises_numbers, index in all_files_to_send:
        await send_screenshots(interaction, files_names, curr_link, exercises_numbers, index)

# Funkcja wykonywana po wpisaniu komendy
async def odrabiamy_get_answers(interaction: discord.Interaction, book, page):
    """Robi zrzuty ekranu zadań z podręcznika i strony wpisanej w argumentach komendy"""

    all_files_to_send = make_screenshots(book, page)

    await send_all_screenshots(interaction, all_files_to_send)
