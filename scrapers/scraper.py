import requests
import json
from math import ceil
import time
import datetime
import os.path
import psycopg2
import logging

def days_hours_minutes(timeDelta):
    return timeDelta.days, timeDelta.seconds//3600, (timeDelta.seconds//60)%60


class Scraper(object):

    def __init__(self):
        self.limit = 1000
        self.maxAttempts = 3
        self.timeMeasurements = []
        self.timeSlot = -1
        self.timeAverage = 0

    def start(self):
        self.before()
        self.run()
        self.close()

    def before(self):
        logging.warning("WARNING: before not implemented")

    def run(self):
        page = 0
        attempt = 1

        while self.hasNext(page):
            try:
                startTime = time.time()
                self.scrape(page, self.limit)
                passedTime = time.time() - startTime
                self.addTimeMeasurement(passedTime)
                self.printProgress(page, passedTime)

                page += 1
                attempt = 1
                logging.info("moving to %d" % (page,))

            except IOError, e:
                logging.exception("attempt %d resulted in an IOError" % attempt)
                attempt += 1
                if attempt <= self.maxAttempts:
                    logging.warning("retrying")
                else:
                    logging.error("more than %d failed attempts, aborting" % self.maxAttempts)
                    break

    def scrape(self, page, limit):

        content = self.fetch(page, limit)
        self.write(content, page)

        return

    def hasNext(page):
        raise NotImplementedError("Subclasses should implement this!")

    def fetch(self, page, limit):
        raise NotImplementedError("Subclasses should implement this!")

    def write(self, json_string, page):
        raise NotImplementedError("Subclasses should implement this!")

    def close(self):
        logging.warning("WARNING: close not implemented")

    def addTimeMeasurement(self, seconds):
        self.timeSlot = (self.timeSlot + 1) % 5
        if len(self.timeMeasurements) > self.timeSlot:
            self.timeMeasurements[self.timeSlot] = seconds
        else:
            self.timeMeasurements.append(seconds)
        totalTime = 0
        for measurement in self.timeMeasurements:
            totalTime += measurement
        self.timeAverage = totalTime / len(self.timeMeasurements)

    def printProgress(self, page, passedTime):
        timeDelta = datetime.timedelta(seconds=passedTime)
        logging.info("duration: %s" % timeDelta)


class WFSScraper(Scraper):
    def __init__(self, basePath, typeName, fileName, sortBy):
        super(WFSScraper, self).__init__()
        self.basePath = basePath
        self.typeName = typeName
        self.fileName = fileName
        self.sortBy = sortBy
        self.totalPages = -1

    def fetch(self, page, limit):
        startIndex = page * limit
        if(self.sortBy is None):
            url = '{}?SERVICE=WFS&request=getFeature&typeName={}&outputFormat=json&srsName=urn:x-ogc:def:crs:EPSG:4326&count={}&startIndex={}'.format(self.basePath, self.typeName, limit, startIndex)
        else:
            url = '{}?SERVICE=WFS&request=getFeature&typeName={}&outputFormat=json&srsName=urn:x-ogc:def:crs:EPSG:4326&count={}&startIndex={}&sortBy={}'.format(self.basePath, self.typeName, limit, startIndex, self.sortBy)

        logging.info('fetching: %s' % url)
        response = requests.get(url, timeout=60)
        content = response.text
        return content

    def write(self, json_string, page):
        indexedFilename = "%s.%d" % (self.fileName, page)

        logging.info('writing: %s' % indexedFilename)
        out = open(indexedFilename, 'wb')
        out.write(bytes(json_string))
        out.close()

        if self.totalPages == -1:
            data = json.loads(json_string)
            self.totalPages = ceil(data["totalFeatures"] / self.limit)
        try:
            logging.info('writing to db')
            self.writeToDb(json_string)
        except Exception as e:
            logging.exception("could not write to database")

    def writeToDb(self, json_string):
        logging.warning("WARNING: writeToDb not implemented")

    def hasNext(self, currentPage):
        if self.totalPages == -1:
            return True
        else:
            return currentPage < self.totalPages

    def printProgress(self, page, passedTime):
        pagesLeft = self.totalPages - page
        timeDelta = datetime.timedelta(seconds=pagesLeft * self.timeAverage)
        logging.info("Time remaining: %s" % timeDelta)


class FileScraper(Scraper):
    def __init__(self, basePath):
        super(FileScraper, self).__init__()
        self.basePath = basePath

    def fetch(self, page, limit):
        fileName = "%s.%d" % (self.basePath , page)

        logging.info('loading: %s' % fileName)
        content = open(fileName).read()
        return content

    def hasNext(self, currentPage):
        fileName = "%s.%d" % (self.basePath, currentPage)
        return os.path.isfile(fileName)

    def write(self, json_string, page):
        raise NotImplementedError("Subclasses should implement this!")
