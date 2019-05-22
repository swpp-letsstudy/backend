from django.contrib import admin

from study.study_user_settings.models import StudyUserSetting
from study.study_groups.models import StudyGroup
from study.study_group_notices.models import StudyGroupNotice
from study.policies.models import Policy
from study.fines.models import Fine
from study.study_meetings.models import StudyMeeting
from study.study_meeting_notices.models import StudyMeetingNotice
from study.attendances.models import Attendance
from study.study_files.models import StudyFile
from study.study_tests.models import StudyTest


admin.site.register(StudyUserSetting)
admin.site.register(StudyGroup)
admin.site.register(StudyGroupNotice)
admin.site.register(Policy)
admin.site.register(Fine)
admin.site.register(StudyMeeting)
admin.site.register(StudyMeetingNotice)
admin.site.register(Attendance)
admin.site.register(StudyFile)
admin.site.register(StudyTest)
