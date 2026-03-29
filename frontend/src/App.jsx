import { useEffect, useState } from 'react'
import AuthPage from './pages/AuthPage'
import BookList from './components/BookList'
import BookDetail from './components/BookDetail'
import RecommendationSection from './components/RecommendationSection'
import { api, setAuthToken } from './services/api'

export default function App() {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  })
  const [books, setBooks] = useState([])
  const [selectedBook, setSelectedBook] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const [message, setMessage] = useState('')

  const loadBooks = async (search = '') => {
    const { data } = await api.get('/books', { params: search ? { search } : {} })
    setBooks(data)
  }

  const loadRecommendations = async (userId) => {
    if (!userId) return
    const { data } = await api.get(`/recommendations/${userId}`)
    setRecommendations(data.recommendations)
  }

  useEffect(() => {
    if (user) {
      loadBooks()
      loadRecommendations(user.id)
    }
  }, [user])

  const handleTrack = async (book, metrics) => {
    await api.post('/track-behavior', {
      user_id: user.id,
      book_id: book.id,
      ...metrics,
    })
    setMessage('Behavior tracked successfully')
    await loadRecommendations(user.id)
  }

  const logout = () => {
    setUser(null)
    setAuthToken(null)
    localStorage.removeItem('user')
    setBooks([])
    setRecommendations([])
  }

  if (!user) {
    return (
      <div className="container">
        <h1>MicroLibrary</h1>
        <AuthPage onAuth={setUser} />
      </div>
    )
  }

  return (
    <div className="container">
      <div className="row between">
        <h1>MicroLibrary</h1>
        <button onClick={logout}>Logout</button>
      </div>
      {message && <p className="success">{message}</p>}
      <div className="layout">
        <BookList books={books} onSelect={setSelectedBook} onSearch={loadBooks} />
        <BookDetail book={selectedBook} onTrack={handleTrack} />
      </div>
      <RecommendationSection recommendations={recommendations} />
    </div>
  )
}
