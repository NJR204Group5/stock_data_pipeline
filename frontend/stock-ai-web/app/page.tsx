"use client";

import { useState } from "react";

export default function Home() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [docs, setDocs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [stockData, setStockData] = useState<any>(null);

  async function handleAsk() {
    if (!question) return;
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/rag/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
          }),
        }
      );

      const data = await response.json();
      console.log(data);
      setStockData(data.stock_data);
      setAnswer(data.answer);
      setDocs(data.retrieved_docs || []);
    } catch (error) {
      console.error(error);
      setAnswer("Error calling API");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-10">

      <h1 className="text-5xl font-bold mb-10">
        AI Stock Assistant
      </h1>

      <div className="flex gap-2 mb-6">

        <input
          className="border p-4 w-full text-2xl rounded"
          placeholder="Ask something..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          onClick={handleAsk}
          className="bg-white text-black px-6 py-4 rounded font-bold"
        >
          Ask
        </button>

      </div>

      {loading && (
        <p className="text-xl">
          Loading...
        </p>
      )}

      {answer && (
        <div className="border p-6 rounded mt-4">
          <h2 className="text-3xl font-bold mb-6">
            AI Answer
          </h2>

          <p className="text-2xl leading-relaxed">
            {answer}
          </p>
        </div>
      )}

      {stockData && (
        <div className="border p-6 rounded mt-6">
          <h2 className="text-3xl font-bold mb-6">
            Technical Indicators
          </h2>

          <div className="grid grid-cols-2 gap-4 text-lg">
            <p>Stock: {stockData.stock_code} {stockData.stock_name}</p>
            <p>Date: {stockData.trade_date}</p>
            <p>Close: {stockData.close}</p>
            <p>MA5: {stockData.ma5}</p>
            <p>MA20: {stockData.ma20}</p>
            <p>MA60: {stockData.ma60}</p>
            <p>Trend: {stockData.trend_type}</p>
            <p>Cross Signal: {stockData.cross_signal}</p>
            <p>Daily Return: {stockData.daily_return}</p>
            <p>Cumulative Return: {stockData.cumulative_return}</p>
          </div>
        </div>
      )}

      {docs.length > 0 && (
        <div className="border p-6 rounded mt-6">
          <h2 className="text-3xl font-bold mb-6">
            Retrieved Documents
          </h2>

          <div className="space-y-4">
            {docs.map((doc, index) => (
              <div
                key={index}
                className="border p-4 rounded"
              >

                <p className="text-sm opacity-70 mb-2">
                  Source: {doc.source_name}
                </p>

                <p className="text-lg leading-relaxed">
                  {doc.chunk_text}
                </p>

                <p className="text-sm opacity-70 mt-3">
                  Distance: {doc.distance}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  );
}