export default function BookList({ books, onSelect, onSearch }) {
  return (
    <div className="card">
      <div className="row between">
        <h3>Books</h3>
        <input placeholder="Search books" onChange={(e) => onSearch(e.target.value)} />
      </div>
      <div className="grid">
        {books.map((book) => (
          <button className="book-card" key={book.id} onClick={() => onSelect(book)}>
            <h4>{book.title}</h4>
            <p>{book.author}</p>
            <span>{book.genre}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
