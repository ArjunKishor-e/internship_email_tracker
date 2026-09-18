import { useState, useEffect } from 'react'
import './App.css'

const STAGE_LABELS = {
  Applied: 'Applied',
  Assessment: 'Assessment',
  Interview: 'Interview',
  Offered: 'Offered',
  Rejected: 'Rejected',
}

function App() {
  const [applications, setApplications] = useState(null)
  const [analytics, setAnalytics] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/applications')
      .then((response) => response.json())
      .then((data) => {
        setApplications(data.applications)
        setAnalytics(data.analytics)
      })
  }, [])

  const loading = applications === null

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
                <th>Link</th>
              </tr>
            </thead>
            <tbody>
              {applications.map((app) => (
                <tr key={app.gmail_thread_id}>
                  <td className="company">
                    {app.company}
                    {app.role_title && <span className="role-title">{app.role_title}</span>}
                  </td>
                  <td>
                    <span
                      className={`stage-badge${app.current_stage === 'Rejected' ? ' rejected' : ''}`}
                    >
                      {app.current_stage}
                    </span>
                  </td>
                  <td>
                    {app.gmail_thread_id && (
                      <a
                        className="email-link"
                        href={`https://mail.google.com/mail/u/0/#all/${app.gmail_thread_id}`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        View email
                      </a>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default App
