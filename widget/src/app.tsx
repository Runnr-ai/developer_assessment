import { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <button
      type="button"
      className="btn btn-primary btn-sm"
      onClick={() => setCount(count + 1)}
    >
      Increment: {count}
    </button>
  );
}
