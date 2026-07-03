import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

// jsdom doesn't implement scrollIntoView and webgl context
window.HTMLElement.prototype.scrollIntoView = function() {};
window.HTMLCanvasElement.prototype.getContext = () => {};

describe('Mutual Fund Assistant UI', () => {
  it('renders the header and disclaimer', () => {
    render(<App />);
    expect(screen.getByText('Mutual Fund Assistant')).toBeInTheDocument();
    expect(screen.getByText('Facts-only. No investment advice.')).toBeInTheDocument();
  });

  it('renders the chat input and send button', () => {
    render(<App />);
    expect(screen.getByPlaceholderText('Ask about any mutual fund...')).toBeInTheDocument();
    // Assuming the send button has the text 'send' (from the google material icon)
    expect(screen.getByText('send')).toBeInTheDocument();
  });

  it('renders the interactive example buttons', () => {
    render(<App />);
    expect(screen.getByText('Check NAV')).toBeInTheDocument();
    expect(screen.getByText('Exit Load')).toBeInTheDocument();
    expect(screen.getByText('Subjective Query')).toBeInTheDocument();
  });

  it('allows clicking an example query to fill the input', () => {
    render(<App />);
    const navBtn = screen.getByText('Check NAV');
    fireEvent.click(navBtn);
    
    // Check if the input contains the query
    // Wait, the sendQuery function in App.jsx triggers the fetch immediately. 
    // We can at least check if the user bubble appeared.
    expect(screen.getByText('What is the NAV of Nippon India small cap?')).toBeInTheDocument();
  });
});
