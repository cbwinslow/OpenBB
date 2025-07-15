import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Trading component', () => {
  render(<App />);
  const linkElement = screen.getByText(/Trading/i);
  expect(linkElement).toBeInTheDocument();
});
