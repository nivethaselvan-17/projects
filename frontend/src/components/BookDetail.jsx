import { useState } from 'react'

export default function BookDetail({ book, onTrack }) {
  const [form, setForm] = useState({ time_spent_minutes: 15, pages_read: 10, click_frequency: 1, liked: false, saved: false })

  if (!book) {
    return <div className="card"><p>Select a book to see details.</p></div>
  }

  return (
    <div className="card">
      <h3>{book.title}</h3>
      <p><strong>Author:</strong> {book.author}</p>
      <p><strong>Genre:</strong> {book.genre}</p>
      <p>{book.description}</p>
      <h4>Track reading behavior</h4>
      <div className="behavior-form">
        <label>
          Time spent (min)
          <input type="number" min="0" value={form.time_spent_minutes} onChange={(e) => setForm({ ...form, time_spent_minutes: Number(e.target.value) })} />
        </label>
        <label>
          Pages read
          <input type="number" min="0" value={form.pages_read} onChange={(e) => setForm({ ...form, pages_read: Number(e.target.value) })} />
        </label>
        <label>
          Click frequency
          <input type="number" min="0" value={form.click_frequency} onChange={(e) => setForm({ ...form, click_frequency: Number(e.target.value) })} />
        </label>
        <label><input type="checkbox" checked={form.liked} onChange={(e) => setForm({ ...form, liked: e.target.checked })} /> Liked</label>
        <label><input type="checkbox" checked={form.saved} onChange={(e) => setForm({ ...form, saved: e.target.checked })} /> Saved</label>
      </div>
      <button onClick={() => onTrack(book, form)}>Submit behavior</button>
    </div>
  )
}
