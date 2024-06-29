from datetime import datetime, timedelta

class botInfo:
    def __init__(self):
        self.events = []
        self.bootTime = datetime.now()

    def logEvent(self):
        self.events.append(datetime.now())

    def getStatistics(self):
        timeNow = datetime.now()
        time24hAgo = timeNow - timedelta(hours=24)
        if time24hAgo < self.bootTime:
            logCut = self.bootTime
        else:
            logCut = time24hAgo
        eventsInLast24h = [event for event in self.events if event >= logCut]
        numEventsInLast24h = len(eventsInLast24h)

        return {
            'total_events': len(self.events),
            'events_last_24h': numEventsInLast24h,
            'bootTime': self.bootTime,
            'logCut': logCut,
            'currentTime': timeNow
        }

    def getFormattedStatistics(self):
        stats = self.getStatistics()
        bootTime = stats['bootTime'].strftime("%c")
        currentTime = stats['currentTime'].strftime("%c")
        logCut = stats['logCut'].strftime("%c")
        return f"Boot Time: {bootTime}\nSystem Time: {currentTime}\nTotal requests recorded: {stats['total_events']}\nRequests in the last 24 hours(since {logCut}): {stats['events_last_24h']}"