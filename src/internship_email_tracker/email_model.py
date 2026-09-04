class Email:
    def __init__(self, company, subject, date, stage):
        self.company = company
        self.subject = subject
        self.date = date
        self.stage = stage
    
    def __str__(self):
        return f"Company:{self.company} ,Subject:{self.subject} ,Date:{self.date} ,Stage:{self.stage}"

if __name__ == "__main__":
    email1 = Email("Amazon", "Online assessment invitation", "Sep 2", "Assessment")
    print(email1.company)
    print(email1.subject)