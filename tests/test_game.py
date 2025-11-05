import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000/")
    driver.maximize_window()
    yield driver
    driver.quit()

def test_keyboard_rendered(driver):
    """Check that all 26 alphabet buttons are rendered."""
    keyboard_buttons = driver.find_elements(By.CSS_SELECTOR, ".keyboard button")
    assert len(keyboard_buttons) == 26

def test_hint_displayed(driver):
    """Verify that the hint text is visible and non-empty."""
    hint_element = driver.find_element(By.CSS_SELECTOR, ".hint-text b")
    assert hint_element.is_displayed()
    assert len(hint_element.text.strip()) > 0

def test_guess_updates_incorrect_counter(driver):
    """Click a wrong letter and ensure the incorrect guess counter increments."""
    wrong_count_before = driver.find_element(By.CSS_SELECTOR, ".guesses-text b").text
    wrong_count_before = int(wrong_count_before.split("/")[0])

    # Find a letter unlikely to exist — e.g., 'z'
    z_button = driver.find_element(By.XPATH, "//button[text()='z']")
    z_button.click()
    time.sleep(1)

    wrong_count_after = driver.find_element(By.CSS_SELECTOR, ".guesses-text b").text
    wrong_count_after = int(wrong_count_after.split("/")[0])

    assert wrong_count_after == wrong_count_before + 1

def test_button_disables_after_click(driver):
    """Ensure that a letter button becomes disabled after clicking."""
    button_a = driver.find_element(By.XPATH, "//button[text()='a']")
    button_a.click()
    time.sleep(0.5)
    assert button_a.get_attribute("disabled") == "true"

def test_game_over_modal_shows(driver):
    """Simulate losing the game and check the modal appears."""
    buttons = driver.find_elements(By.CSS_SELECTOR, ".keyboard button:not([disabled])")
    for btn in buttons:
        btn.click()
        time.sleep(0.2)
        guesses = driver.find_element(By.CSS_SELECTOR, ".guesses-text b").text
        wrong_count = int(guesses.split("/")[0])
        if wrong_count == 6:
            break

    modal = driver.find_element(By.CSS_SELECTOR, ".game-modal")
    assert "show" in modal.get_attribute("class")

def test_play_again_button_resets_game(driver):
    """Click 'Play Again' and verify the game resets."""
    play_again = driver.find_element(By.CSS_SELECTOR, ".play-again")
    play_again.click()
    time.sleep(1)

    modal = driver.find_element(By.CSS_SELECTOR, ".game-modal")
    assert "show" not in modal.get_attribute("class")

    guesses_text = driver.find_element(By.CSS_SELECTOR, ".guesses-text b").text
    assert guesses_text.startswith("0")