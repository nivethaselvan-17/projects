export default function RecommendationSection({ recommendations }) {
  return (
    <div className="card">
      <h3>Recommended for you</h3>
      {recommendations.length === 0 ? (
        <p>No recommendations yet. Interact with books first.</p>
      ) : (
        recommendations.map((item) => (
          <div className="rec-item" key={item.book_id}>
            <h4>{item.title}</h4>
            <p>{item.author}</p>
            <p>Score: {item.score}</p>
            <ul>
              {item.reasons.map((reason, idx) => <li key={idx}>{reason}</li>)}
            </ul>
          </div>
        ))
      )}
    </div>
  )
}
