from django.db import models

class Record(models.Model):
    timestamp = models.IntegerField()
    avg_ask = models.FloatField()
    avg_bid = models.FloatField()
    
    def write_to_db(self, record):
        self.avg_ask = record.get("avg_ask")
        self.avg_bid = record.get("avg_bid")
        self.timestamp = record.get("timestamp")        
        self.save()

    def to_dict(self):
        return {
            "avg_ask": self.avg_ask,
            "avg_bid": self.avg_bid,
            "timestamp": self.timestamp
        }
