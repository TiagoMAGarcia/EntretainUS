from datetime import datetime
from django.db import models
from django.contrib.auth.forms import User


class Challenge(models.Model):
    CHALLENGES_TYPES = (('programming', 'Programming Challenge'),
                        ('gaming', 'Gaming Challenge'),
                        ('sports', 'Sports Challenge'),
                        ('Culinary', 'Culinary Challenge'),
                        ('music', 'Music Challenge'),
                        ('makeup', 'MakeUp Challenge'))

    title = models.CharField(max_length=100)
    challenge_user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=15)
    content = models.CharField(max_length=1000, blank=True)
    image = models.URLField(blank=True, null=True)
    challenge_type = models.CharField(max_length=11, choices=CHALLENGES_TYPES)
    video = models.CharField(max_length=150, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    challenge_likes = models.ManyToManyField(User, related_name='like', blank=True)

    def get_title(self):
        return self.title

    def get_challenge_type(self):
        return self.challenge_type

    def get_tag(self):
        return self.tag

    def get_user(self):
        return self.challenge_user

    def get_content(self):
        return self.content

    def get_image(self):
        return self.image

    def get_video(self):
        return self.video

    def get_date(self):
        time = datetime.now()
        if self.date.minute == 0:
            return str(time.second - self.date.second) + "seg ago"
        elif (self.date.hour + 1) == time.hour and self.date.day == time.day:
            return str(time.minute - self.date.minute) + "min ago"
        elif self.date.day == time.day and self.date.month == time.month:
            if time.hour - (self.date.hour + 1) == 1:
                return str(time.hour - (self.date.hour + 1)) + " hour ago"
            return str(time.hour - (self.date.hour + 1)) + " hours ago"
        else:
            if self.date.month == time.month:
                if time.day - self.date.day == 1:
                    return str(time.day - self.date.day) + " day ago"
                return str(time.day - self.date.day) + " days ago"

        return self.date

    def get_challenge_likes(self):
        return self.challenge_likes.all().count()


class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    comment_challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=False)
    comment_likes = models.ManyToManyField(User, related_name='comment_like', blank=True)
    text = models.CharField(max_length=1000, blank=True)
    comment_date = models.DateTimeField(auto_now_add=True)

    def get_comment_user(self):
        return self.comment_user

    def get_comment_likes(self):
        return self.comment_likes.all().count()

    def get_text(self):
        return self.text

    def get_comment_date(self):
        time = datetime.now()
        if self.comment_date.minute == 0:
            return str(time.second - self.comment_date.second) + "seg ago"
        elif (self.comment_date.hour + 1) == time.hour and self.comment_date.day == time.day:
            return str(time.minute - self.comment_date.minute) + "min ago"
        elif self.comment_date.day == time.day and self.comment_date.month == time.month:
            if time.hour - (self.comment_date.hour + 1) == 1:
                return str(time.hour - (self.comment_date.hour + 1)) + " hour ago"
            return str(time.hour - (self.comment_date.hour + 1)) + " hours ago"
        else:
            if self.comment_date.month == time.month:
                if time.day - self.comment_date.day == 1:
                    return str(time.day - self.comment_date.day) + " day ago"
                return str(time.day - self.comment_date.day) + " days ago"

        return self.comment_date