import { useState, useEffect, Fragment } from 'react'
import './App.css'
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const STAGE_LABELS = {
  Applied: 'Applied',
  Assessment: 'Assessment',
  Interview: 'Interview',
  AssessmentCentre: 'Assessment Centre',
  Offered: 'Offered',
  Rejected: 'Rejected',
}

const STAGE_SORT_ORDER = ['Applied', 'Assessment', 'Interview', 'AssessmentCentre', 'Offered', 'Rejected']

function App() {
  const [applications, setApplications] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [expandedThreadId, setExpandedThreadId] = useState(null)
  const [syncing, setSyncing] = useState(false)
  const [toast, setToast] = useState(null)
  const [loadError, setLoadError] = useState(false)
  const [search, setSearch] = useState('')
  const [sortKey, setSortKey] = useState('company')
  const [sortDir, setSortDir] = useState('asc')
  const [demoMode, setDemoMode] = useState(false)

  function loadApplications() {
    setLoadError(false)
    fetch(`${API_URL}/api/applications`)
      .then((response) => response.json())
      .then((data) => {
        setApplications(data.applications)
        setAnalytics(data.analytics)
        setDemoMode(data.demo_mode === true)
      })
      .catch(() => setLoadError(true))
  }

  useEffect(() => {
    loadApplications()
  }, [])

  useEffect(() => {
    const timer = setInterval(() => {
      fetch(`${API_URL}/api/applications`)
        .then((response) => response.json())
        .then((data) => {
          setApplications(data.applications)
          setAnalytics(data.analytics)
        })
        .catch(() => {})
    }, 60000)
    return () => clearInterval(timer)
  }, [])

  function toggleExpanded(threadId) {
    setExpandedThreadId(expandedThreadId === threadId ? null : threadId)
  }

  function handleSync() {
    setSyncing(true)
    setToast(null)
    fetch(`${API_URL}/sync`)
      .then((response) => response.json())
      .then((result) => {
        setToast(`Synced ${result.emails_checked} emails, ${result.new_applications} new`)
        loadApplications()
      })
      .catch(() => setToast('Sync failed, try again'))
      .finally(() => setSyncing(false))

    setTimeout(() => setToast(null), 5000)
  }

  const loading = applications === null

  function handleSort(key) {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
  }

  function sortIndicator(key) {
    if (sortKey !== key) return ''
    return sortDir === 'asc' ? ' ▲' : ' ▼'
  }

  const query = search.trim().toLowerCase()
  const visibleApplications = (applications || [])
    .filter((app) => {
      if (!query) return true
      const text = [
        app.company,
        app.role_title,
        STAGE_LABELS[app.current_stage] || app.current_stage,
        ...app.emails.map((email) => email.subject),
      ].join(' ').toLowerCase()
      return text.includes(query)
    })
    .sort((a, b) => {
      let result = 0
      if (sortKey === 'company') {
        result = a.company.toLowerCase().localeCompare(b.company.toLowerCase())
      } else if (sortKey === 'stage') {
        result = STAGE_SORT_ORDER.indexOf(a.current_stage) - STAGE_SORT_ORDER.indexOf(b.current_stage)
      } else if (sortKey === 'emails') {
        result = a.emails.length - b.emails.length
      }
      return sortDir === 'asc' ? result : -result
    })

  return (
    <div className="app">
      <div className="page">
        <header>
          <h1>Internship Tracker</h1>
          {demoMode ? (
            <span className="demo-badge">Demo data</span>
          ) : (
            <button className="sync-link" onClick={handleSync} disabled={syncing}>
              {syncing ? 'Syncing…' : 'Sync emails'}
            </button>
          )}
        </header>

        {toast && <p className="toast">{toast}</p>}
        {demoMode && (
          <p className="toast">This is a demo with made-up data. The real version connects to your Gmail.</p>
        )}

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
                {applications && applications.length > 0 && (
          <input
            className="search"
            type="text"
            placeholder="Search company, role, stage or email subject"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        )}
        {loadError && <p className="empty">Couldn't reach the backend. Is it running?</p>}

        {!loadError && loading && <p className="loading">Loading applications…</p>}

        {!loadError && !loading && applications.length > 0 && visibleApplications.length === 0 && (
          <p className="empty">No applications match your search</p>
        )}

        {!loadError && !loading && applications.length > 0 && (
          <table>
            <thead>
              <tr>
                <th className="sortable" onClick={() => handleSort('company')}>Company{sortIndicator('company')}</th>
                <th className="sortable" onClick={() => handleSort('stage')}>Stage{sortIndicator('stage')}</th>
                <th className="sortable" onClick={() => handleSort('emails')}>Emails{sortIndicator('emails')}</th>
              </tr>
            </thead>
            <tbody>
              {visibleApplications.map((app) => (
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
