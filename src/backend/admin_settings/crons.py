# import datetime
#
# from decouple import config
# from django.utils import timezone
#
# from .models import Organization, SubscriptionPlan, OrganizationPlan, DemoMeeting
# from .serializers import OrganizationPlanSerializer
# from .services import get_active_plans, interkt_send_message
#
# from ..base.services import create_update_record
# from ..base.utils.timezone import now_local, to_localtime
#
#
# # cronjob for giving basic plan
# def auto_basic_plan():
#     courts = Organization.objects.filter(is_active=True)
#     default_obj = SubscriptionPlan.objects.filter(is_default=True, is_active=True).first()
#     today = now_local(only_date=True)
#     for record in courts:
#         queryset = OrganizationPlan.objects.filter(plan__is_default=True, is_active=True, is_completed=True,
#                                                    court=record.id)
#         queryset = get_active_plans(queryset)
#         if not queryset.exists():
#             data = {"court": record.id, "plan": default_obj.id, "start_date": today, "is_active": True}
#             create_update_record(data, OrganizationPlanSerializer, OrganizationPlan)
#
#
# def meetings_three_hour():
#     three_hours_from_now = now_local() + timezone.timedelta(minutes=180)
#     one_hour_from_now = now_local() + timezone.timedelta(minutes=60)
#     # Get all active meetings scheduled two hours from now and not more than 30 minutes from now
#     meetings_to_run = DemoMeeting.objects.filter(is_active=True, date__lte=three_hours_from_now,
#                                                  date__gte=one_hour_from_now)
#     for meeting in meetings_to_run:
#         template = config('INTERAKT_DEMO_3') if to_localtime(meeting.date).hour == 15 else config('INTERAKT_DEMO_5')
#         if meeting.mobile:
#             interkt_send_message(meeting.mobile, template, [])
#
#
# def meetings_one_hour():
#     one_hour_from_now = now_local() + timezone.timedelta(minutes=60)
#     five_minutes_from_now = now_local() + timezone.timedelta(minutes=5)
#     # Get all active meetings scheduled 30 minutes from now and not more than 5 minutes from now
#     meetings_30_min_away = DemoMeeting.objects.filter(is_active=True, date__lte=one_hour_from_now,
#                                                       date__gte=five_minutes_from_now)
#     for meeting in meetings_30_min_away:
#         template = config('INTERAKT_DEMO_3') if to_localtime(meeting.date).hour == 15 else config('INTERAKT_DEMO_5')
#         if meeting.mobile:
#             interkt_send_message(meeting.mobile, template, [])
#
#
# def meetings_five_minutes():
#     five_minutes_from_now = now_local() + timezone.timedelta(minutes=5)
#     meetings_5_min_away = DemoMeeting.objects.filter(is_active=True, date__lte=five_minutes_from_now,
#                                                      date__gte=datetime.datetime.now())
#     for meeting in meetings_5_min_away:
#         if meeting.mobile:
#             template = config('INTERAKT_DEMO_3') if to_localtime(meeting.date).hour == 15 else config('INTERAKT_DEMO_5')
#             interkt_send_message(meeting.mobile, template, [])
