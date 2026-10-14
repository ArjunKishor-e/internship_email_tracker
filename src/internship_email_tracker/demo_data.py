from internship_email_tracker.models import Application

DEMO_EMAILS = [
    {"id": "demo-001", "thread_id": "demo-t-nw", "company": "Northwind Labs", "sender_domain": "northwind.example",
     "date": "Mon, 7 Sep 2026 09:12:00 +0000",
     "subject": "Application received: Software Engineering Placement 2027",
     "body": "Thank you for applying to Northwind Labs. We have received your application and will be in touch."},
    {"id": "demo-002", "thread_id": "demo-t-nw", "company": "Northwind Labs", "sender_domain": "northwind.example",
     "date": "Fri, 11 Sep 2026 10:30:00 +0000",
     "subject": "Next step: complete your online assessment",
     "body": "Please complete your online assessment within 7 days using the link below."},
    {"id": "demo-003", "thread_id": "demo-t-nw", "company": "Northwind Labs", "sender_domain": "northwind.example",
     "date": "Tue, 22 Sep 2026 14:05:00 +0000",
     "subject": "Interview invitation - Software Engineering Placement",
     "body": "Well done on the assessment. We would like to arrange a video call with the engineering team."},
    {"id": "demo-004", "thread_id": "demo-t-nw", "company": "Northwind Labs", "sender_domain": "northwind.example",
     "date": "Fri, 2 Oct 2026 16:45:00 +0000",
     "subject": "Job offer: Software Engineering Placement",
     "body": "We are pleased to offer you a place on our 2027 placement scheme. Congratulations!"},

    {"id": "demo-005", "thread_id": "demo-t-bw", "company": "Brightwave Systems", "sender_domain": "brightwave.example",
     "date": "Tue, 8 Sep 2026 11:00:00 +0000",
     "subject": "Thanks for your application - Data Analyst Internship",
     "body": "Your submission has gone through and the team will review it shortly."},
    {"id": "demo-006", "thread_id": "demo-t-bw", "company": "Brightwave Systems", "sender_domain": "brightwave.example",
     "date": "Mon, 14 Sep 2026 09:00:00 +0000",
     "subject": "Online assessment invitation",
     "body": "Please complete your online assessment. It takes about 45 minutes."},
    {"id": "demo-007", "thread_id": "demo-t-bw", "company": "Brightwave Systems", "sender_domain": "brightwave.example",
     "date": "Wed, 23 Sep 2026 15:20:00 +0000",
     "subject": "An update on your application",
     "body": "Unfortunately we will not be taking your application further this time. Thank you for your interest."},

    {"id": "demo-008", "thread_id": "demo-t-hx", "company": "Helix Robotics", "sender_domain": "helix.example",
     "date": "Wed, 9 Sep 2026 13:40:00 +0000",
     "subject": "Application confirmation: Embedded Software Intern",
     "body": "Thanks for submitting your details. We will review them over the coming weeks."},
    {"id": "demo-009", "thread_id": "demo-t-hx", "company": "Helix Robotics", "sender_domain": "helix.example",
     "date": "Thu, 17 Sep 2026 10:10:00 +0000",
     "subject": "Technical test: Helix Robotics",
     "body": "Please complete your technical test within five days."},
    {"id": "demo-010", "thread_id": "demo-t-hx", "company": "Helix Robotics", "sender_domain": "helix.example",
     "date": "Mon, 5 Oct 2026 09:30:00 +0000",
     "subject": "You are invited to our assessment day",
     "body": "The day runs from 9am to 4pm at our Bristol office. Please confirm your attendance."},

    {"id": "demo-011", "thread_id": "demo-t-ar", "company": "Ardent Bank", "sender_domain": "ardent.example",
     "date": "Thu, 10 Sep 2026 08:15:00 +0000",
     "subject": "Application received - Technology Summer Internship",
     "body": "Thank you for applying to Ardent Bank. We will contact you if you are shortlisted."},

    {"id": "demo-012", "thread_id": "demo-t-ke1", "company": "Kestrel Aerospace", "sender_domain": "kestrel.example",
     "date": "Fri, 11 Sep 2026 12:00:00 +0000",
     "subject": "Application received: Year in Industry Engineering Placement",
     "body": "Thank you for applying to Kestrel Aerospace. We have received your application."},
    {"id": "demo-013", "thread_id": "demo-t-ke2", "company": "Kestrel Aerospace", "sender_domain": "kestrel.example",
     "date": "Tue, 6 Oct 2026 11:25:00 +0000",
     "subject": "Interview scheduled: Year in Industry Engineering",
     "body": "Your panel is booked for next Thursday at 2pm. Details are attached."},

    {"id": "demo-014", "thread_id": "demo-t-or", "company": "Orbit Payments", "sender_domain": "orbit.example",
     "date": "Mon, 14 Sep 2026 16:00:00 +0000",
     "subject": "Application received - Backend Engineering Intern",
     "body": "Thank you for applying to Orbit Payments. We have received your application."},
    {"id": "demo-015", "thread_id": "demo-t-or", "company": "Orbit Payments", "sender_domain": "orbit.example",
     "date": "Fri, 25 Sep 2026 09:50:00 +0000",
     "subject": "Your application outcome",
     "body": "We regret to inform you that you have not been successful on this occasion."},

    {"id": "demo-016", "thread_id": "demo-t-dl", "company": "Delta Logistics", "sender_domain": "delta.example",
     "date": "Tue, 15 Sep 2026 10:00:00 +0000",
     "subject": "Application confirmation: Software Engineering Intern",
     "body": "Thanks for applying to Delta Logistics. We have received your application."},
    {"id": "demo-017", "thread_id": "demo-t-dl", "company": "Delta Logistics", "sender_domain": "delta.example",
     "date": "Wed, 7 Oct 2026 13:15:00 +0000",
     "subject": "Action required: complete your assessment",
     "body": "Please follow the link to begin. The assessment closes in seven days."},

    {"id": "demo-018", "thread_id": "demo-t-ce", "company": "Cedar Health", "sender_domain": "cedar.example",
     "date": "Wed, 16 Sep 2026 14:30:00 +0000",
     "subject": "Application received - Software Placement 2027",
     "body": "Thank you for applying to Cedar Health. We have received your application."},

    {"id": "demo-019", "thread_id": "demo-t-fg", "company": "Forage", "sender_domain": "theforage.com",
     "date": "Thu, 17 Sep 2026 07:30:00 +0000",
     "subject": "Forage / Alex - A new internship programme just opened",
     "body": ""},
    {"id": "demo-020", "thread_id": "demo-t-nl", "company": "Tech Weekly", "sender_domain": "techweekly.example",
     "date": "Fri, 18 Sep 2026 06:00:00 +0000",
     "subject": "This week in tech: five stories worth reading",
     "body": "Your weekly digest of news from across the industry."},
]


def seed_demo_data(db):
    session = db.Session()
    already_seeded = session.query(Application).count() > 0
    session.close()

    if already_seeded:
        return

    db.process_emails(list(reversed(DEMO_EMAILS)))