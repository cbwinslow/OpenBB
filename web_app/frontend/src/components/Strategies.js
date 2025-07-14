import React, { useState, useEffect } from "react";
import { getStrategies } from "../api";

const Strategies = () => {
  const [strategies, setStrategies] = useState([]);

  useEffect(() => {
    getStrategies().then((data) => {
      setStrategies(data);
    });
  }, []);

  return (
    <div>
      <h1>Strategies</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Rule IDs</th>
          </tr>
        </thead>
        <tbody>
          {strategies.map((strategy) => (
            <tr key={strategy.id}>
              <td>{strategy.id}</td>
              <td>{strategy.name}</td>
              <td>{strategy.rule_ids.join(", ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Strategies;
