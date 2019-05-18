from django.db import models
from django.contrib.auth.models import User


class StudyUser(User):
    # username
    # password
    info = models.CharField(max_length=50)
    # study_groups_own  StudyGroup          1:N
    # study_groups_join StudyGroup          N:N
    # group_notices     StudyGroupNotice    1:N
    # fines             Fine                1:N
    # study_meetings    StudyMeeting        N:N
    # meeting_notices   StudyMeetingNotice  1:N
    # attendances       Attendance          1:N
    # files             StudyFile           1:N
    # tests             StudyTest           1:N


class StudyGroup(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=20)
    info = models.CharField(default='', max_length=100)
    owner = models.ForeignKey(StudyUser, related_name='study_groups_own', on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(StudyUser, related_name='study_groups_join')
    # notices           StudyGroupNotice    1:N
    # policies          Policy              1:N
    # meetings          StudyMeeting        1:N
    # files             StudyFeil           1:N
    # tests             StudyTest           1:N


class StudyGroupNotice(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.title
    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)
    writer = models.ForeignKey(StudyUser, related_name='group_notices', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudyGroup, related_name='notices', on_delete=models.CASCADE)


class Policy(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.name
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=20)
    group = models.ForeignKey(StudyGroup, related_name='policies', on_delete=models.CASCADE)
    # fines     Fine    1:N


class Fine(models.Model):
    class Meta:
        ordering = ('created',)
    created = models.DateTimeField(auto_now_add=True)

    amount = models.IntegerField(default=0)
    user = models.ForeignKey(StudyUser, related_name='fines', on_delete=models.CASCADE, null=True)
    policy = models.ForeignKey(Policy, related_name='fines', on_delete=models.CASCADE)

class StudyMeeting(models.Model):
    class Meta:
        ordering = ('time',)
    def __str__(self):
        return self.time
    created = models.DateTimeField(auto_now_add=True)

    time = models.DateTimeField()
    info = models.CharField(default='', max_length=100)
    group = models.ForeignKey(StudyGroup, related_name='meetings', on_delete=models.CASCADE)
    members = models.ManyToManyField(StudyUser, related_name='study_meetings')
    # notices       StudyMeetingNotice  1:N
    # attendances   Attendance          1:N
    # tests         StudyTest           1:N


class StudyMeetingNotice(models.Model):
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.title
    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=200)
    writer = models.ForeignKey(StudyUser, related_name='meeting_notices', on_delete=models.CASCADE, null=True)
    meeting = models.ForeignKey(StudyMeeting, related_name='notices', on_delete=models.CASCADE)


class Attendance(models.Model):
    class Meta:
        ordering = ('created',)
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(StudyUser, related_name='attendances', on_delete=models.CASCADE)
    meeting = models.ForeignKey(StudyMeeting, related_name='attendances', on_delete=models.CASCADE)


class StudyFile(models.Model):
    class Meta:
        ordering = ('created',)
    created = models.DateTimeField(auto_now_add=True)

    filepath = models.CharField(max_length=200)
    owner = models.ForeignKey(StudyUser, related_name='files', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudyGroup, related_name='files', on_delete=models.CASCADE)


class StudyTest(models.Model):
    class Meta:
        ordering = ('created',)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    title = models.CharField(max_length=20)
    owner = models.ForeignKey(StudyUser, related_name='tests', on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(StudyGroup, related_name='tests', on_delete=models.CASCADE)
    meeting = models.ForeignKey(StudyMeeting, related_name='tests', on_delete=models.CASCADE)

