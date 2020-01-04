from super_bbs.controller.v1.account.api import LoginAPI, LoginOutAPI, RegisterAPI, ProfileAPI, \
    GetCaptchaHandler, CaptchaCheckAPI, SendEmailAPI, LoginStatusCheck, UpdatePasswordAPI
from super_bbs.controller.v1.index.api import IndexMixedAPI
from super_bbs.controller.v1.topic.api import TopicAPI, TopicUpDownCountAPI, TopicAppendAPI, TopicCommentAPI, \
    TopicFavAPI, TopicThankAPI, CommentThankAPI, TopicAddView, UserFavAPI
from super_bbs.controller.v1.tabs.api import TabMixedAPI, SubTabAPI, TabAPI, SubTabFavAPI
from super_bbs.controller.v1.member.api import MemberIndexAPI, MemberTopicAPI, MemberCommentAPI

routers = [
    # account
    ('/account/login', LoginAPI, 'account_login'),
    ('/account/register', RegisterAPI, 'account_register'),
    ('/account/logout', LoginOutAPI, 'account_logout'),
    ('/account/check', LoginStatusCheck, 'account_login_status_check'),
    ('/account/profile', ProfileAPI, 'account_profile'),
    ('/account/password', UpdatePasswordAPI, 'account_password'),
    # captcha
    ('/captcha', GetCaptchaHandler, 'captcha_get'),
    ('/captcha/check', CaptchaCheckAPI, 'captcha_check'),
    # send email
    ('/email/send', SendEmailAPI, 'email_send'),
    ('/index', IndexMixedAPI, 'index'),
    ('/go', TabMixedAPI, 'go'),
    ('/tab', TabAPI, 'tab'),
    ('/sub_tab', SubTabAPI, 'sub_tab'),
    ('/sub_tab/fav', SubTabFavAPI, 'sub_tab_fav'),
    ('/topic', TopicAPI, 'topic'),
    ('/topic/append', TopicAppendAPI, 'topic_append'),
    ('/topic/fav', TopicFavAPI, 'topic_fav'),
    ('/topic/view', TopicAddView, 'topic_view'),
    ('/topic/thank', TopicThankAPI, 'topic_thank'),
    ('/topic/comment', TopicCommentAPI, 'topic_comment'),
    ('/topic/comment/thank', CommentThankAPI, 'topic_comment_thank'),
    ('/topic/up_down', TopicUpDownCountAPI, 'topic_up_down'),
    ('/user/fav', UserFavAPI, 'user_fav'),
    ('/member', MemberIndexAPI, 'member'),
    ('/member/topic', MemberTopicAPI, 'member_topic'),
    ('/member/comment', MemberCommentAPI, 'member_comment'),
]
