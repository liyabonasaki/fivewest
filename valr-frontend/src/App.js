import React, { useState } from 'react';


function App(pr) {
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState(null);
  const [error, setError] = useState('');

  const fetchPrice = async () => {
    try {
      setError('');
      const response = await fetch(`http://127.0.0.1:9000/price?quantity=${quantity}`);
      const data = await response.json();
      if (response.ok) {
        setPrice(data.price);
      } else {
        setError(data.detail || 'Failed to fetch price');
      }
    } catch (error) {
      setError('Error fetching price');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: 'auto' }}>
      <h1>USDT to ZAR Price Calculator</h1>
      <label htmlFor="quantity">USDT Amount to buy:</label>
      <input
        id="quantity"
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        placeholder="Enter USDT quantity"
        style={{ width: '100%', padding: '8px', marginTop: '8px', marginBottom: '16px' }}
      />
      <button onClick={fetchPrice} style={{ padding: '10px', width: '100%' }}>
        Get Price
      </button>
      {error && <p style={{ color: 'red', marginTop: '16px' }}>{error}</p>}
      {price !== null && (
        <p style={{ marginTop: '16px', fontSize: '18px' }}>
          Price: <strong>{price} ZAR</strong>
        </p>
      )}
    </div>
  );
}

export default App;
