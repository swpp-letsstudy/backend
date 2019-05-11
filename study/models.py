from django.db import models
from django.contrib.auth.models import User

# User: username, password, groups

class StudyGroup(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, related_name='study_groups_own', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='study_groups_join')
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=100)
    # meetings
    # noticies
    # policies


class StudyGroupNotice(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.title
    created = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(StudyGroup, related_name='notices', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)


class StudyGroupPolicy(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(StudyGroup, related_name='policies', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    # fines


class StudyMeeting(models.Model):
    class Meta:
        ordering = ('time',)
    def __str__(self):
        return self.time
    created = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(StudyGroup, related_name='study_meetings', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='study_meetings')
    time = models.DateTimeField()
    info = models.CharField(default='', max_length=100)
    # noticies


class StudyMeetingNotice(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.contents
    created = models.DateTimeField(auto_now_add=True)

    meeting = models.ForeignKey(StudyMeeting, related_name='notices', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)


class Fine(models.Model):
    class Meta:
        ordering = ('created',)
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='fines', on_delete=models.CASCADE)
    policy = models.ForeignKey(StudyGroupPolicy, related_name='fines', on_delete=models.CASCADE)
    meeting = models.ForeignKey(StudyMeeting, related_name='fines', on_delete=models.CASCADE)


class Attendance(models.Model):
    class Meta:
        ordering = ('created',)
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='attendances', on_delete=models.CASCADE)
    meeting = models.ForeignKey(StudyMeeting, related_name='attendances', on_delete=models.CASCADE)

