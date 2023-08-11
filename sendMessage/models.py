from django.db import models

# Create your models here.
class Batch(models.Model):
    class mediaTypes(models.TextChoices):
        TELEGRAM = "Telegram"
        MAIL = "Mail"
        BOTH = "BOTH"
    class statusTypes(models.TextChoices):
        SUCCESS = "success"
        FAILURE = "failure"

        
    sender = models.CharField(max_length=20, null=False)
    message = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(auto_now_add=True)
    mediaType = models.CharField(
                    max_length=10,
                    choices=mediaTypes.choices,
                    default="Telegram"
                )
    status = models.CharField(
                    max_length=20,
                    choices=statusTypes.choices,
                    default=None
                )
    statusCode = models.IntegerField(default=None) 
    groupName = models.CharField(max_length=100, default="Automated school notifier", null=True)
    messageID = models.IntegerField(default=None, null=True)
    chatID = models.IntegerField(default=None, null=True)
    errorCode = models.IntegerField(default=None, null=True)
    errorDescription = models.CharField(max_length=100, default=None, null=True)
    
    def __str__(self):  
        return str(self.time)

    def api_dict(self):
        retval = {}
        retval['sender'] = self.sender
        retval['message'] = self.message
        retval['time'] = self.time
        retval['mediaType'] = self.mediaType
        retval['status'] = self.status
        retval['statusCode'] = self.statusCode
        retval['groupName'] = self.groupName
        retval['messageID'] = self.messageID
        retval['chatID'] = self.chatID
        retval['errorCode'] = self.errorCode
        retval['errorDescription'] = self.errorDescription
        return retval
    
    def __repr__(self):
        return self