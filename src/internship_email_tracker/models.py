from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)  # placeholder for future multi-user support
    company = Column(String)
    role_title = Column(String, nullable=True)
    gmail_thread_id = Column(String, unique=True, nullable=True)
    current_stage = Column(String, default="Applied")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    status_history = relationship("StatusHistory", back_populates="application")
    emails = relationship("EmailRecord", back_populates="application")


class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    stage = Column(String)
    changed_at = Column(DateTime, default=datetime.utcnow)
    source_email_id = Column(Integer, ForeignKey("emails.id"), nullable=True)

    application = relationship("Application", back_populates="status_history")


class EmailRecord(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)
    gmail_id = Column(String, unique=True)
    company = Column(String)
    subject = Column(String)
    date = Column(String)
    stage = Column(String)

    application = relationship("Application", back_populates="emails")