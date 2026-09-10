import { useState, useEffect } from 'react'

function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/applications')
      .then((response) => response.json())
      .then((json) => setData(json))
  }, [])

  return (
    <div>
      <h1>Internship Tracker</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

export default App