
from typing import Optional
from datetime import datetime
from termcolor import colored

class ConsoleHandler:
    COLORS = {
        "CRITICAL": (227, 7, 7),
        "ERROR": (255, 80, 80),
        "WARNING": (255, 100, 40),
        "INFO": (100, 185, 255),
        "DEBUG": (120, 55, 30)
    }
    
    def emit(self, level, msg):
        print(
            colored(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]", color="green"), 
            colored(level, color=self.COLORS.get(level, "white"), attrs=["bold"]), 
            colored(msg, color="white")
        )
            
class FileHandler:
    def __init__(self, filename: str):
        self.filename = filename

    def emit(self, level, msg):
        try:
            with open(self.filename, "a") as file:
                file.write(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {level} {msg}\n")
        except Exception as e:
            print(colored(f"failed to write log to {self.filename}: {e}", color="red"))

class Logger:
    LEVELS = {
        "CRITICAL":50,
        "ERROR":40,
        "WARNING":30,
        "INFO":20,
        "DEBUG":10,
    }
    
    def __init__(
        self,
        log_path: Optional[str] = None,
        level: str = "DEBUG",
    ):
        self.level = self.LEVELS[level]
        self.handlers = [ConsoleHandler()]
        
        if log_path:
            self.handlers.append(FileHandler(log_path))
    
    def log(self, level, msg):
        if self.LEVELS[level] >= self.level:
            for handler in self.handlers:
                handler.emit(level, msg)
    
    def critical(self, msg): self.log("CRITICAL", msg)
    def error(self, msg): self.log("ERROR", msg)
    def warning(self, msg): self.log("WARNING", msg)
    def info(self, msg): self.log("INFO", msg)
    def debug(self, msg): self.log("DEBUG", msg)