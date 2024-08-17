import os
import art
from loguru import logger

if __name__ == "__main__":
    asicii_art = art.text2art("Vanilla Client")
    print (asicii_art)

    from initialization import env,hook,onebot
