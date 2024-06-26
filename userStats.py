from datetime import datetime, timedelta

class UsageStatistics:
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
        return f"Boot Time: {stats['bootTime'].strftime("%c")}\nSystem Time: {stats['currentTime'].strftime("%c")}\nTotal requests recorded: {stats['total_events']}\nRequests in the last 24 hours(since {stats['logCut'].strftime("%c")}): {stats['events_last_24h']}"