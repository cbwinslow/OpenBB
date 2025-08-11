import React, { useState } from 'react';
import { getPrices } from '../api';
import Chart from './Chart';

const Trading = () => {
  const [symbol, setSymbol] = useState('AAPL');
  const [data, setData] = useState([]);

  const handleFetch = async () => {
    const prices = await getPrices(symbol);
    setData(prices);
  };

  return (
    <div>
      <h1>Trading</h1>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
      />
      <button onClick={handleFetch}>Fetch</button>
      {data.length > 0 && <Chart data={data} />}
    </div>
  );
};

export default Trading;
