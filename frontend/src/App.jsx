import { useState, useEffect, Fragment } from 'react'
import './App.css'

const STAGE_LABELS = {
  Applied: 'Applied',
  Assessment: 'Assessment',
  Interview: 'Interview',
  AssessmentCentre: 'Assessment Centre',
  Offered: 'Offered',
  Rejected: 'Rejected',
}

function App() {
  const [applications, setApplications] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [expandedThreadId, setExpandedThreadId] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/applications')
      .then((response) => response.json())
      .then((data) => {
        setApplications(data.applications)
        setAnalytics(data.analytics)
      })
  }, [])

  const loading = applications === null

  function toggleExpanded(threadId) {
    setExpandedThreadId(expandedThreadId === threadId ? null : threadId)
  }

  return (
    <div className="app">
      <div className="page">
        <header>
          <h1>Internship Tracker</h1>
          <a className="sync-link" href="http://127.0.0.1:8000/sync">
            Sync emails
          </a>
        </header>

        {analytics && (
          <div className="summary">
            {Object.entries(STAGE_LABELS).map(([stage, label]) => (
              <div className="stat" key={stage}>
                <strong>
                  {Math.round((analytics.conversion_rates?.[stage] ?? 0) * analytics.total_applications)}
                </strong>
                {label}
              </div>
            ))}
          </div>
        )}

        {loading && <p className="loading">Loading applications…</p>}

        {!loading && applications.length === 0 && (
          <p className="empty">No applications yet. Sync your emails to get started.</p>
        )}

        {!loading && applications.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Company</th>
                <th>Stage</th>
                <th>Emails</th>
              </tr>
            </thead>
            <tbody>
              {applications.map((app) => (
                <Fragment key={app.gmail_thread_id}>
                  <tr>
                    <td className="company">
                      {app.company}
                      {app.role_title && <span className="role-title">{app.role_title}</span>}
                    </td>
                    <td>
                      <span
                        className={`stage-badge${app.current_stage === 'Rejected' ? ' rejected' : ''}`}
                      >
                        {STAGE_LABELS[app.current_stage] || app.current_stage}
                      </span>
                    </td>
                    <td>
                      <button
                        className="expand-button"
                        onClick={() => toggleExpanded(app.gmail_thread_id)}
                      >
                        {expandedThreadId === app.gmail_thread_id ? '▾' : '▸'} {app.emails.length} email{app.emails.length === 1 ? '' : 's'}
                      </button>
                    </td>
                  </tr>
                  {expandedThreadId === app.gmail_thread_id && (
                    <tr className="email-dropdown-row">
                      <td colSpan={3}>
                        <table className="email-dropdown">
                          <thead>
                            <tr>
                              <th>Subject</th>
                              <th>Stage</th>
                              <th></th>
                            </tr>
                          </thead>
                          <tbody>
                            {app.emails.map((email) => (
                              <tr key={email.gmail_id}>
                                <td>{email.subject}</td>
                                <td>
                                  <span className="stage-badge">
                                    {STAGE_LABELS[email.stage] || email.stage}
                                  </span>
                                </td>
                                <td>
                                  <a
                                    className="email-link"
                                    href={`https://mail.google.com/mail/u/0/#all/${email.gmail_id}`}
                                    target="_blank"
                                    rel="noreferrer"
                                  >
                                    View
                                  </a>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default App
