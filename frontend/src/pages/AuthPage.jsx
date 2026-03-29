import { useState } from 'react'
import { api, setAuthToken } from '../services/api'

export default function AuthPage({ onAuth }) {
  const [isSignup, setIsSignup] = useState(true)
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [error, setError] = useState('')

  const submit = async (event) => {
    event.preventDefault()
    setError('')

    try {
      const endpoint = isSignup ? '/signup' : '/login'
      const payload = isSignup ? form : { email: form.email, password: form.password }
      const { data } = await api.post(endpoint, payload)
      setAuthToken(data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      onAuth(data.user)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Authentication failed')
    }
  }

  return (
    <div className="card auth-card">
      <h2>{isSignup ? 'Create account' : 'Welcome back'}</h2>
      <form onSubmit={submit}>
        {isSignup && (
          <input
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
        )}
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />
        {error && <p className="error">{error}</p>}
        <button type="submit">{isSignup ? 'Sign up' : 'Login'}</button>
      </form>
      <p>
        {isSignup ? 'Already have an account?' : "Don't have an account?"}{' '}
        <button className="link-btn" onClick={() => setIsSignup(!isSignup)}>
          {isSignup ? 'Login' : 'Sign up'}
        </button>
      </p>
    </div>
  )
}
