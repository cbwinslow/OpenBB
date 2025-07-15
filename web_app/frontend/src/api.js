const API_URL = "http://localhost:8000";

export const getRoot = async () => {
  const response = await fetch(`${API_URL}/`);
  const data = await response.json();
  return data;
};

export const getStrategies = async () => {
    const response = await fetch(`${API_URL}/strategies`);
    const data = await response.json();
    return data;
};

export const postQuestion = async (question) => {
    const response = await fetch(`${API_URL}/chatbot?question=${question}`, {
        method: "POST",
    });
    const data = await response.json();
    return data;
};

export const getPrices = async (symbol) => {
    const response = await fetch(`${API_URL}/prices/${symbol}`);
    const data = await response.json();
    return data;
}
