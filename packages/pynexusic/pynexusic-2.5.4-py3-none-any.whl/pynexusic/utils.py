import os
import webbrowser
import logging
from enum import Enum
from collections import deque as DQ

#######################################################################################################
def launchDocs():
    """
        Launches documentation in the default OS browser

        :return: No return
    """
    ROOT_DIR = (os.path.dirname(os.path.abspath(__file__)))
    url = os.path.join(ROOT_DIR, 'docs/index.html')
    url = 'file://' + url
    new = 2  # open in a new tab, if possible
    webbrowser.open(url, new=new)

#######################################################################################################
def print_log(msg, logger=None, logLvl=logging.INFO):
    """
        Print message to console and log in logger

        :param msg: (``string``) - Message to be printed
        :param logger: (``Logger`` - optional) - Logger variable to be used to print in log file (default value None)
        :param logLvel: (``int`` - optional) - Logging level number (default value logging.INFO, which is equivalent to 20)

        :return: No return
    """
    print(msg)

    if logger != None:
        logger.log(logLvl, msg)

#######################################################################################################
def setup_logger(name, log_file, formatter=None, logLvl=logging.INFO):
    """
        Setup logger to create a log file

        :param name: (``string``) - Name of the logger
        :param log_file: (``string``) - Name of the log file
        :param formatter: (``string`` - optional) - Format of the log file (default value None)
        :param logLvel: (``int`` - optional) - Logging level number (default value logging.INFO, which is equivalent to 20)

        :return: (``Logger``) - Logger object
    """
    if formatter == None:
        formatter = ('%(asctime)s - [%(levelname)s] %(message)s')

    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(logging.Formatter(formatter))
    logger = logging.getLogger(name)
    logger.setLevel(logLvl)
    logger.addHandler(handler)
    return logger

#######################################################################################################
def isXMLValid(data: str):
    """
        Check if an XML string is valid or not. Also provide the invalid tags and elements

        :param data: (``string``) - XML string to be checked.

        :return: (``tuple`` - bool, dict) - The first item in the tuple is whether the string is a valid XML or not. The second item is a dictionary of missingTags and missingChars.
    """

    # State enum definition
    class State(Enum):
        CLOSED_TAG = 1
        OPEN_TAG = 2
        ELEM_NAME = 3

    class MissingType(Enum):
        START_TAG = 'Missing Start Tag'
        END_TAG = 'Missing End Tag'
        START_CHAR = 'Missing Start Tag Char'
        END_CHAR = 'Missing End Tag Char'

    # Check validity class using DFA
    class CheckValidity():
        def __init__(self, data):
            self.data = data
            self.currState = State.CLOSED_TAG
            self.startChars = DQ()
            self.missingChars = []
            self.startTags = DQ()
            self.missingTags = []

        # Move to OPEN_TAG state
        def moveToOt(self, char: str, idx: int):
            self.startChars.append((char, idx, MissingType.END_CHAR))
            self.currState = State.OPEN_TAG

        # Move to CLOSED_TAG state
        def moveToCt(self, char: str, idx: int):
            if len(self.startChars) == 0:
                self.missingChars.append((char, idx, MissingType.START_CHAR))
            else:
                self.startChars.pop()
            self.currState = State.CLOSED_TAG

        # Move to ELEM_NAME state
        def moveToEN(self, char: str, idx: int):
            startIdx = self.startChars[-1][1]
            elementName = self.data[startIdx + 1: idx]
            endTag = (elementName, startIdx, idx, MissingType.START_TAG)
            potentialMiss = DQ()
            found = False

            if elementName[0] == '/':
                while len(self.startTags) > 0:
                    startTag = self.startTags.pop()
                    if startTag[0] != elementName[1: len(elementName)]:
                        potentialMiss.appendleft(startTag)
                    else:
                        found = True
                        break

                if found:
                    self.missingTags.extend(potentialMiss)
                else:
                    self.missingTags.append(endTag)
                    self.startTags = potentialMiss
            else:
                self.startTags.append((elementName, startIdx, idx, MissingType.END_TAG))

            if char == '>':
                self.moveToCt(char, idx)
            else:
                self.currState = State.ELEM_NAME

        # Start processing
        def process(self):
            for idx, char in enumerate(self.data):
                if self.currState == State.CLOSED_TAG:
                    if char == '<':
                        self.moveToOt(char, idx)
                    elif char == '>':
                        self.moveToCt(char, idx)
                elif self.currState == State.OPEN_TAG:
                    if char == ' ' or char == '>':
                        self.moveToEN(char, idx)
                    elif char == '<':
                        self.moveToOt(char, idx)
                elif self.currState == State.ELEM_NAME:
                    if char == '>':
                        self.moveToCt(char, idx)
                    elif char == '<':
                        self.moveToOt(char, idx)

            # Get remaining missed start tags
            while len(self.startTags) > 0:
                tag = self.startTags.pop()
                self.missingTags.append(tag)

            # Get remaining missed start chars
            while len(self.startChars) > 0:
                tag = self.startChars.pop()
                self.missingChars.append(tag)

            # Check isValid before return
            isValid = True
            if self.currState != State.CLOSED_TAG or \
                len(self.missingTags) > 0 or len(self.missingChars) > 0:
                isValid = False

            return isValid, {'missingTags': self.missingTags, 'missingChars': self.missingChars}

    check = CheckValidity(data)
    return check.process()

#######################################################################################################
if __name__ == '__main__':
    launchDocs()