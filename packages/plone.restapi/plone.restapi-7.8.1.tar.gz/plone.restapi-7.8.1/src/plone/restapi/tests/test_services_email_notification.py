# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING
from plone.restapi.testing import RelativeSession
from Products.MailHost.interfaces import IMailHost
from zope.component import getUtility

import transaction
import unittest


try:
    from Products.CMFPlone.factory import _IMREALLYPLONE5  # noqa
except ImportError:
    PLONE5 = False
else:
    PLONE5 = True


@unittest.skipIf(
    not PLONE5, "email notification not implemented for Plone < 5."
)  # noqa
class EmailNotificationEndpoint(unittest.TestCase):

    layer = PLONE_RESTAPI_DX_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.mailhost = getUtility(IMailHost)

        registry = getUtility(IRegistry)
        registry["plone.email_from_address"] = "info@plone.org"
        registry["plone.email_from_name"] = u"Plone test site"

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        self.anon_api_session = RelativeSession(self.portal_url)
        self.anon_api_session.headers.update({"Accept": "application/json"})

        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def test_email_notification_missing_parameters(self):
        response = self.api_session.post(
            "/@email-notification", json={"message": "Just want to say hi."}
        )
        transaction.commit()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.mailhost.messages, [])
        error = response.json()
        self.assertEqual(error["message"], "Missing from or message parameters")

    def test_email_notification(self):
        response = self.api_session.post(
            "/@email-notification",
            json={"from": "john@doe.com", "message": "Just want to say hi."},
        )
        transaction.commit()

        self.assertEqual(response.status_code, 204)
        msg = self.mailhost.messages[0]
        if isinstance(msg, bytes) and bytes is not str:
            # Python 3 with Products.MailHost 4.10+
            msg = msg.decode("utf-8")
        self.assertTrue("Subject: [No Subject]" in msg)
        self.assertTrue("To: info@plone.org" in msg)
        self.assertTrue("Reply-To: john@doe.com" in msg)
        self.assertTrue("Just want to say hi." in msg)

    def test_email_notification_all_parameters(self):
        response = self.api_session.post(
            "/@email-notification",
            json={
                "from": "john@doe.com",
                "message": "Just want to say hi.",
                "name": "John Doe",
                "subject": "This is the subject.",
            },
        )
        transaction.commit()

        self.assertEqual(response.status_code, 204)
        msg = self.mailhost.messages[0]
        if isinstance(msg, bytes) and bytes is not str:
            # Python 3 with Products.MailHost 4.10+
            msg = msg.decode("utf-8")
        self.assertTrue("=?utf-8?q?This_is_the_subject" in msg)
        self.assertTrue("To: info@plone.org" in msg)
        self.assertTrue("John Doe" in msg)
        self.assertTrue("Reply-To: john@doe.com" in msg)
        self.assertTrue("Just want to say hi." in msg)
