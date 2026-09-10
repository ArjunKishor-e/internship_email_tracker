import { useState, useEffect } from 'react'

function App() {
  const [applications, setApplications] = useState([])
  const [analytics, setAnalytics] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/applications')
      .then((response) => response.json())
      .then((data) => {
        setApplications(data.applications)
        setAnalytics(data.analytics)
      })
  }, [])

  return (
    <div>
      <h1>Internship Tracker</h1>

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
              <td>{app.company}</td>
              <td>{app.current_stage}</td>
              <td>
                <a href={`https://mail.google.com/mail/u/0/#all/${app.gmail_thread_id}`} target="_blank" rel="noreferrer">
                  View email
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default App