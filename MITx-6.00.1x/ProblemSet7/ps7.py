# 6.00.1x Problem Set 7
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *


#-----------------------------------------------------------------------
#
# Problem Set 7

#======================
# Code for retrieving and parsing RSS feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret
#======================

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory:
    def __init__(self, guid, title, subject, summary, link):
        self._guid = guid
        self._title = title
        self._subject = subject
        self._summary = summary
        self._link = link

    def getGuid(self):
        return self._guid
    def getTitle(self):
        return self._title
    def getSubject(self):
        return self._subject
    def getSummary(self):
        return self._summary
    def getLink(self):
        return self._link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self, word):
        self._word = word
    def isWordIn(self, text):
        punctuation = string.punctuation
        #print punctuation
        #print type(punctuation)
        #print type(text)
        for elem in text.split():
            for ind in range(len(elem)-1):
                if elem[ind] == "'":
                    elem = elem[:ind]
                    #print 'AAAA', elem
                    break
            elem = elem.lower()
            elem = filter(lambda x: x not in punctuation, elem)
            #print elem
            #print self._word
            if self._word.lower() == elem:
                return True
        return False

# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    # def __init__(self, word):
    #     self._word = word
    def evaluate(self, newsStory):
        return self.isWordIn(newsStory.getTitle())

# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    def evaluate(self, newsStory):
        return self.isWordIn(newsStory.getSubject())

# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    def evaluate(self, newsStory):
        return self.isWordIn(newsStory.getSummary())


# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        #print type(trigger)
        self._trigger = trigger
    def evaluate(self, news):
        #print news
        return not self._trigger.evaluate(news)


# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self._trigger1 = trigger1
        self._trigger2 = trigger2
    def evaluate(self, news):
        if self._trigger1.evaluate(news) and self._trigger2.evaluate(news):
            return True
        return False
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self._trigger1 = trigger1
        self._trigger2 = trigger2
    def evaluate(self, news):
        if self._trigger1.evaluate(news) or self._trigger2.evaluate(news):
            return True
        return False

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self._phrase = phrase
    def evaluate(self, news):
        if self._phrase in news.getSubject() or \
        self._phrase in news.getSummary() or \
        self._phrase in news.getTitle():
            return True
        return False
#======================
# Part 3
# Filtering
#======================

def filterStories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    new_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) and \
               story not in new_stories:
                new_stories.append(story)
    return new_stories

#======================
# Part 4
# User-Specified Triggers
#======================

def makeTrigger(triggerMap, triggerType, params, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    triggerMap: dictionary with names as keys (strings) and triggers as values
    triggerType: string indicating the type of trigger to make (ex: "TITLE")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"])
    name: a string representing the name of the new trigger (ex: "t1")

    Modifies triggerMap, adding a new key-value pair for this trigger.

    Returns a new instance of a trigger (ex: TitleTrigger, AndTrigger).
    """
    if triggerType == 'TITLE':
        word = ' '.join(params)
        trigger = TitleTrigger(word)
        triggerMap[name] = trigger
        return trigger
    elif triggerType == 'SUBJECT':
        word = ' '.join(params)
        trigger = SubjectTrigger(word)
        triggerMap[name] = trigger
        return trigger
    elif triggerType == 'SUMMARY':
        word = ' '.join(params)
        trigger = SummaryTrigger(word)
        triggerMap[name] = trigger
        return trigger
    
    elif triggerType == 'PHRASE':
        phrase = ' '.join(params)
        trigger = PhraseTrigger(phrase)
        triggerMap[name] = trigger
        return trigger

    elif triggerType == 'NOT':
        trig_name = ' '.join(params)
        trigger = NotTrigger(triggerMap[trig_name])
        triggerMap[name] = trigger
        return trigger
    elif triggerType == 'AND':
        and_trigger = AndTrigger(triggerMap[params[0]], triggerMap[params[1]])
        triggerMap[name] = and_trigger
        return and_trigger
    elif triggerType == 'OR':
        or_trigger = OrTrigger(triggerMap[params[0]],\
                                triggerMap[params[1]])
        triggerMap[name] = or_trigger
        return or_trigger

    # elif triggerType == 'ADD':
    #     pass
    # return 


def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """

    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    triggers = []
    triggerMap = {}

    # Be sure you understand this code - we've written it for you,
    # but it's code you should be able to write yourself
    for line in lines:

        linesplit = line.split(" ")

        # Making a new trigger
        if linesplit[0] != "ADD":
            trigger = makeTrigger(triggerMap, linesplit[1],
                                  linesplit[2:], linesplit[0])

        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(triggerMap[name])

    return triggers
    
import thread
SLEEPTIME = 60 #seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    try:
        # These will probably generate a few hits...
        # t1 = TitleTrigger("Trump")
        # t2 = SubjectTrigger("Romney")
        # t3 = PhraseTrigger("Election")
        # t4 = OrTrigger(t2, t3)
        # triggerlist = [t1, t4]
        
        # TODO: Problem 11
        # After implementing makeTrigger, uncomment the line below:
        triggerlist = readTriggerConfig("triggers.txt")
        print 'Number of finded posts',len(triggerlist)
        # **** from here down is about drawing ****
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        
        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)

        # Gather stories
        guidShown = []
        def get_cont(newstory):
            if newstory.getGuid() not in guidShown:
                cont.insert(END, newstory.getTitle()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.getSummary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.getGuid())

        while True:

            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")
            # for stori in stories:
            #     print stori
            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            # Process the stories
            stories = filterStories(stories, triggerlist)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)


            print "Sleeping..."
            time.sleep(SLEEPTIME)

    except Exception as e:
        print e


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()

