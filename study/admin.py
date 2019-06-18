from django.contrib import admin

from study.study_users.models import StudyUser
from study.study_groups.models import StudyGroup
from study.study_group_notices.models import StudyGroupNotice
from study.policies.models import Policy, Fine
from study.study_meetings.models import StudyMeeting
from study.study_meeting_notices.models import StudyMeetingNotice
from study.attendances.models import Attendance


admin.site.register(StudyUser)
admin.site.register(StudyGroup)
admin.site.register(StudyGroupNotice)
admin.site.register(Policy)
admin.site.register(Fine)
admin.site.register(StudyMeeting)
admin.site.register(StudyMeetingNotice)
admin.site.register(Attendance)

