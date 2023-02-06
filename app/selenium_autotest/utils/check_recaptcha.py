from selenium.webdriver.common.by import By
import speech_recognition as sr
import pydub
import time
import requests
import traceback


def check_captcha(driver, time_delay, log):
    time.sleep(time_delay)
    try:
        log.make_screenshot()
        reCAPTCHA_frame = driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
    except Exception:
        log.add_log("RECAPTCHA: not find captcha", "success")
        return 1
    driver.switch_to.frame(reCAPTCHA_frame)
    log.make_screenshot()
    driver.find_element(By.XPATH, '//*[@id="rc-anchor-container"]').click()
    time.sleep(time_delay)

    # Проверяем прошла ли проверка каптчи просто по клику, если да то будет исключение
    try:
        driver.save_screenshot("captcha.png")
        driver.find_element(By.XPATH, "//div[@class='recaptcha-checkbox-checkmark']").get_attribute("style")
    except Exception:
        log.add_log("RECAPTCHA: recaptcha send without confirm SUCCESS", "success")
        driver.switch_to.default_content()
        time.sleep(time_delay)
        driver.find_element(By.ID, "contact-form-submit").submit()
        return 1
    else:
        driver.switch_to.parent_frame()
        try:
            log.make_screenshot()
            reCAPTCHA_frame_image = driver.find_element(
                By.XPATH, "//iframe[@title='recaptcha challenge " "expires in two minutes']"
            )
        except Exception as exception:
            print("".join(traceback.format_stack()))
            log.add_log("".join(traceback.format_stack()), "{}".format(exception.__getattribute__("msg")))
        else:
            driver.switch_to.frame(reCAPTCHA_frame_image)
            driver.find_element(By.XPATH, "//*[@id='recaptcha-audio-button']").click()
            time.sleep(time_delay)
            while True:
                try:
                    log.make_screenshot()
                    href_audio = driver.find_element(
                        By.XPATH, "//*[@title='Alternatively, " "download audio as MP3']"
                    ).get_attribute("href")
                except Exception:
                    log.make_screenshot()
                    log.add_log("RECAPTCHA: Google understand that you are robot", "failed")
                    return 0
                else:
                    r = sr.Recognizer()
                    con = requests.get(href_audio)
                    bt = con.content
                    with open("so.mp3", "wb") as f:
                        f.write(bt)
                    sound = pydub.AudioSegment.from_mp3("so.mp3")
                    sound.export("soo.wav", format="wav")
                    with sr.AudioFile("soo.wav") as source:
                        # listen for the data (load audio to memory)
                        audio_data = r.record(source)
                        # recognize (convert from speech to text)
                        text = r.recognize_google(audio_data)
                        driver.find_element(By.XPATH, "//*[@id='audio-response']").send_keys(text)
                        driver.find_element(By.XPATH, "//*[@id='recaptcha-verify-button']").click()
                        time.sleep(time_delay)
                        error_text = driver.find_element(By.XPATH, "//div[@class='rc-audiochallenge-error-message']")
                        if error_text.text:
                            driver.find_element(
                                By.XPATH, "//button[@class='rc-button goog-inline-block " "rc-button-reload']"
                            ).click()
                            time.sleep(time_delay)
                            continue
                        else:
                            try:
                                log.make_screenshot()
                                driver.find_element(
                                    By.XPATH, "//div[@class=" "'recaptcha-checkbox-checkmark']"
                                ).get_attribute("style")
                            except Exception:
                                driver.switch_to.parent_frame()
                                log.add_log("RECAPTCHA: audio recaptcha send confirm SUCCESS", "success")
                                return 2
                            else:
                                log.make_screenshot()
                                log.add_log("RECAPTCHA: unknown error FAILED(dont find checkmark)", "failed")
                                return 0
