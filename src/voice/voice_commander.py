# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import speech_recognition as sr
import pyttsx3
from agentscope.agents import DialogAgent, UserAgent
from agentscope.msgs import Msg

# ThÃªm Ä‘Æ°á»ng dáº«n Ä‘á»ƒ import module cá»§a báº¡n
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_db
from src.agents import run_all_agents
from src.learning.real_time_learning import RealTimeLearner

class AIOSVoiceCommander:
    """Voice Agent Ä‘iá»u khiá»ƒn toÃ n bá»™ AI_OS_KERNEL_V3"""
    
    def __init__(self):
        # Khá»Ÿi táº¡o speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Khá»Ÿi táº¡o text-to-speech
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 170)
        self.tts.setProperty('volume', 0.9)
        
        # Khá»Ÿi táº¡o cÃ¡c thÃ nh pháº§n core
        self.learner = RealTimeLearner()
        
        # AgentScope agent
        self.agent = DialogAgent(name="AIOS_Commander", sys_prompt=self._get_system_prompt())
    
    def _get_system_prompt(self):
        return """Báº¡n lÃ  trá»£ lÃ½ Ä‘iá»u khiá»ƒn há»‡ thá»‘ng AI_OS_KERNEL_V3.
        Báº¡n cÃ³ thá»ƒ thá»±c hiá»‡n cÃ¡c lá»‡nh: cháº¡y pipeline, huáº¥n luyá»‡n model, 
        crawl dá»¯ liá»‡u, xem thá»‘ng kÃª chiáº¿n dá»‹ch. HÃ£y pháº£n há»“i ngáº¯n gá»n."""
    
    def speak(self, text):
        """PhÃ¡t Ã¢m thanh pháº£n há»“i"""
        print(f"[AIOS] {text}")
        self.tts.say(text)
        self.tts.runAndWait()
    
    def listen(self):
        """Láº¯ng nghe vÃ  nháº­n diá»‡n giá»ng nÃ³i"""
        with self.microphone as source:
            print("ðŸŽ¤ Äang nghe...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try:
            command = self.recognizer.recognize_google(audio, language="vi-VN")
            print(f"ðŸ“ Nháº­n lá»‡nh: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak("Xin lá»—i, tÃ´i khÃ´ng nghe rÃµ.")
            return None
        except sr.RequestError:
            self.speak("Lá»—i káº¿t ná»‘i dá»‹ch vá»¥ nháº­n diá»‡n.")
            return None
    
    def execute_command(self, command):
        """Thá»±c thi lá»‡nh tá»« giá»ng nÃ³i"""
        if not command:
            return
        
        # Äiá»u khiá»ƒn pipeline
        if "cháº¡y pipeline" in command or "run pipeline" in command:
            self.speak("Äang cháº¡y pipeline...")
            run_all_agents()
            self.speak("Pipeline hoÃ n táº¥t.")
        
        # Huáº¥n luyá»‡n model
        elif "huáº¥n luyá»‡n" in command or "train" in command:
            self.speak("Äang huáº¥n luyá»‡n model dá»± Ä‘oÃ¡n...")
            subprocess.run(["python", "src/ml/train_prediction_model.py"])
            self.speak("Huáº¥n luyá»‡n hoÃ n táº¥t.")
        
        # Crawl dá»¯ liá»‡u
        elif "crawl" in command or "thu tháº­p" in command:
            self.speak("Äang crawl dá»¯ liá»‡u Ä‘á»‘i thá»§...")
            subprocess.run(["python", "src/crawlers/crawl_competitors.py"])
            self.speak("Crawl hoÃ n táº¥t.")
        
        # Xem thá»‘ng kÃª
        elif "thá»‘ng kÃª" in command or "campaign" in command:
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM campaigns")
                count = cur.fetchone()[0]
                self.speak(f"Há»‡ thá»‘ng cÃ³ {count} chiáº¿n dá»‹ch.")
        
        # Khá»Ÿi Ä‘á»™ng web
        elif "web" in command or "dashboard" in command:
            self.speak("Äang khá»Ÿi Ä‘á»™ng web dashboard...")
            subprocess.Popen([sys.executable, "-m", "src.main"])
            self.speak("Dashboard Ä‘Ã£ sáºµn sÃ ng táº¡i cá»•ng 5000.")
        
        # Dá»«ng há»‡ thá»‘ng
        elif "táº¡m dá»«ng" in command or "pause" in command:
            self.speak("Táº¡m dá»«ng há»‡ thá»‘ng.")
            # ThÃªm logic pause
        
        # Lá»‡nh khÃ´ng xÃ¡c Ä‘á»‹nh
        else:
            self.speak("Lá»‡nh khÃ´ng Ä‘Æ°á»£c há»— trá»£. Vui lÃ²ng thá»­ láº¡i.")
    
    def run(self):
        """VÃ²ng láº·p chÃ­nh cá»§a Voice Agent"""
        self.speak("Xin chÃ o! AIOS Voice Commander Ä‘Ã£ sáºµn sÃ ng.")
        self.speak("HÃ£y nÃ³i lá»‡nh cá»§a báº¡n.")
        
        while True:
            command = self.listen()
            if command:
                if "thoÃ¡t" in command or "exit" in command or "táº¡m biá»‡t" in command:
                    self.speak("Táº¡m biá»‡t!")
                    break
                self.execute_command(command)

if __name__ == "__main__":
    commander = AIOSVoiceCommander()
    commander.run()

